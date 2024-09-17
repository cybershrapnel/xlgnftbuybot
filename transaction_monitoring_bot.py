import os
import requests
import time
import base58
import hashlib
import asyncio
from playwright.async_api import async_playwright

# Contract address for $XLG
XLG_contract_address = "TQr5axvJzETeHsUiXv6QjBEh1BKH571AZu"
username = "xlgnftbuybot"

# The specific contract address for the deck we want to filter
specific_deck_address = "TDuEK3tqCn9YPFNAFd7SDypdqDisNXm1xr"

# Folder where images are stored
images_folder = "images"

# Path to the txids.txt file
txids_file = "txids.txt"

# TronGrid API endpoint with pagination
base_url = "https://api.trongrid.io/v1/contracts/{}/transactions"

# Function to load processed transaction IDs from file
def load_processed_txids():
    if os.path.exists(txids_file):
        with open(txids_file, "r") as f:
            return set(line.strip() for line in f)
    return set()

# Function to save a new transaction ID to the file
def save_processed_txid(tx_id):
    with open(txids_file, "a") as f:
        f.write(f"{tx_id}\n")

# Function to fetch contract transactions with a limit and optional timestamp filter
def get_contract_transactions(limit=200, start_timestamp=None):
    url = f"{base_url.format(XLG_contract_address)}?limit={limit}"
    if start_timestamp:
        url += f"&min_timestamp={start_timestamp}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get('data', []), None
        else:
            print(f"Failed to fetch data, status code: {response.status_code}")
            return [], None
    except Exception as e:
        print(f"Error fetching contract transactions: {e}")
        return [], None

# Function to fetch transaction details by ID
def fetch_transaction_details(tx_id):
    try:
        url = f"https://api.trongrid.io/v1/transactions/{tx_id}/events"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch transaction details, status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching transaction details: {e}")
        return None

# Function to convert hex Ethereum-style address to base58 Tron address
def hex_to_base58(hex_address):
    address_with_prefix = '41' + hex_address[2:]
    address_bytes = bytes.fromhex(address_with_prefix)
    hash1 = hashlib.sha256(address_bytes).digest()
    hash2 = hashlib.sha256(hash1).digest()
    checksum = hash2[:4]
    address_with_checksum = address_bytes + checksum
    base58_address = base58.b58encode(address_with_checksum).decode()
    return base58_address

# Function to format transaction summary (switching buyer and seller labels)
def format_transaction_summary(transaction_data, tx_id):
    if transaction_data and 'data' in transaction_data:
        for event in transaction_data['data']:
            # We check if the contract address is our specific deck address
            if event['caller_contract_address'] == specific_deck_address and event['event_name'] == 'OrdersMatched':
                event_params = event.get('result', {})
                buyer_hex = event_params.get('maker', 'N/A')  # Originally buyer
                seller_hex = event_params.get('taker', 'N/A')  # Originally seller
                trx_amount = int(event_params.get('price', 0)) / 1_000_000 if event_params.get('price') else 'N/A'
                buyer_address = hex_to_base58(buyer_hex) if buyer_hex != 'N/A' else 'N/A'
                seller_address = hex_to_base58(seller_hex) if seller_hex != 'N/A' else 'N/A'

                # Switch buyer and seller
                transaction_summary = (
                    "Buyer: " + seller_address + "\n"  # Maker is the seller
                    "Seller: " + buyer_address + "\n"  # Taker is the buyer
                    "Amount: " + str(trx_amount) + " TRX\n"
                    "Transaction ID: " + tx_id + "\n"
                    "Deck: " + specific_deck_address + "\n"  # Specify deck name as the specific contract address
                )
                return transaction_summary
    return None

# Function to format transfer details (including token ID)
def format_transfer_details(transaction_data):
    transfer_details = ""
    token_id = None
    if transaction_data and 'data' in transaction_data:
        for event in transaction_data['data']:
            # We check if the contract address is our specific deck address
            if event['caller_contract_address'] == specific_deck_address and event['event_name'] == 'Transfer':
                event_params = event.get('result', {})
                token_id = event_params.get('tokenId', 'N/A')
                transfer_details += (
                    "Item Sold (Token ID): " + str(token_id) + "\n"
                    "Deck: $XLG\n"  # Specify deck name as $XLG
                )
    return transfer_details, token_id

# Function to simulate typing into a contenteditable div
async def type_text(page, selector, value):
    try:
        await page.click(selector)  # Focus on the element
        await page.fill(selector, "")  # Clear any existing content
        for char in value:
            await page.keyboard.press(char)  # Type each character
    except Exception as e:
        print(f"Failed to type text: {e}")

# Function to get the TRX spent for a specific transaction using TronScan API
def get_trx_spent_on_transaction(tx_id):
    try:
        # TronScan API endpoint for transaction details
        url = f"https://apilist.tronscanapi.com/api/transaction-info?hash={tx_id}"
        response = requests.get(url)

        if response.status_code == 200:
            tx_info = response.json()
            total_trx_spent = 0

            if 'transfersAllList' in tx_info:
                # Iterate over transfers and sum up TRX spent
                for transfer in tx_info['transfersAllList']:
                    if transfer['symbol'] == "TRX":
                        amount_spent = int(transfer['amount_str']) / 1_000_000  # Convert from sun to TRX
                        total_trx_spent += amount_spent

                return total_trx_spent
            else:
                print("No TRX transfers found in this transaction.")
                return None
        else:
            print(f"Failed to fetch transaction data, status code: {response.status_code}")
            return None

    except Exception as e:
        print(f"Error fetching transaction data: {e}")
        return None

# Function to attach an image if it exists in the folder
async def attach_image_if_exists(page, token_id):
    if token_id:
        image_path = os.path.join(images_folder, f"{token_id}.jpg")
        if os.path.exists(image_path):
            print(f"Attaching image: {image_path}")
            await page.set_input_files('input[type="file"]', image_path)
            await page.wait_for_timeout(2000)  # Wait 2 seconds to ensure the image upload completes
        else:
            print(f"No image found for Token ID: {token_id}")

# Function to post transaction details
async def post_transaction_details(page, transaction_data, tx_id):
    try:
        # Raw data output for debugging
        print(f"\nProcessing Transaction ID: {tx_id}")
        print(f"Raw Transaction Data:\n{transaction_data}")

        # Initialize variables for OrdersMatched and Transfer event details
        transaction_summary = None
        transfer_details = None
        should_process = False  # Flag to determine if we should process this transaction
        buyer_address = None
        seller_address = None
        token_id = None

        # Loop through the transaction data to find the matching events
        for event in transaction_data.get('data', []):
            # Check if the caller_contract_address matches your deck
            if event['caller_contract_address'] == specific_deck_address:
                should_process = True  # We found our deck, so we need to process this transaction

            # Process OrdersMatched event for transaction summary and addresses
            if event['event_name'] == 'OrdersMatched':
                print("Processing OrdersMatched event...")
                transaction_summary = format_transaction_summary(transaction_data, tx_id)
                event_params = event.get('result', {})
                buyer_address = hex_to_base58(event_params.get('maker', 'N/A'))  # Maker (seller)
                seller_address = hex_to_base58(event_params.get('taker', 'N/A'))  # Taker (buyer)

            # Process Transfer event and get token_id
            if event['event_name'] == 'Transfer':
                print("Processing Transfer event...")
                transfer_details, token_id = format_transfer_details(transaction_data)

        # Retrieve the total TRX spent using the new API
        total_trx_spent = get_trx_spent_on_transaction(tx_id)
        trx_spent_str = f"\nTotal TRX Spent: {total_trx_spent} TRX\n" if total_trx_spent is not None else ""

        # Buyer and seller string
        buyer_seller_str = f"Buyer: {buyer_address}\nSeller: {seller_address}\n" if buyer_address and seller_address else ""

        # If the caller_contract_address matches, we process the transaction, regardless of missing events
        if should_process and (transaction_summary or transfer_details):
            post_content = f"Transaction ID: {tx_id}\n{transaction_summary or ''}{transfer_details or ''}{buyer_seller_str}{trx_spent_str}"

            print("Clicking the 'Post' button to open the post dialog...")
            await page.click('a[aria-label="Post"][role="link"]')
            await page.wait_for_selector('input[type="file"]', timeout=10000)

            # Type in the transaction details by simulating key presses
            await type_text(page, 'div[contenteditable="true"][role="textbox"]', post_content)

            # Attach the image if available
            await attach_image_if_exists(page, token_id)

            # Wait a little more before posting to ensure image uploads
            await page.wait_for_timeout(3000)

            print("Clicking the 'Post' button to submit the post...")
            await page.click('button[data-testid="tweetButton"]')
            await page.wait_for_timeout(3000)
            print(f"Post submitted successfully for transaction ID: {tx_id}")

            # Save the processed transaction ID to the file to avoid reposting
            save_processed_txid(tx_id)
        else:
            print(f"Skipping post for transaction ID: {tx_id} because it doesn't match the required conditions.")

    except Exception as e:
        print(f"Failed to post transaction details for transaction ID: {tx_id}: {e}")

# Main function to process and post existing transactions
async def process_existing_transactions(page):
    print("Fetching existing transactions...")

    # Load processed transaction IDs
    processed_txids = load_processed_txids()

    # Manually add the transaction ID to process
    transaction_ids = ["0c943af20dec1668fca83c9cb35b2b5ebd094db09a41796e865e2a11765008d8"]
    
    for tx_id in transaction_ids:
        if tx_id not in processed_txids:  # Skip if the transaction is already processed
            print(f"\nProcessing manually added transaction: {tx_id}")
            transaction_data = fetch_transaction_details(tx_id)
            if transaction_data:
                await post_transaction_details(page, transaction_data, tx_id)
        else:
            print(f"Transaction ID {tx_id} already processed. Skipping.")

    # Continue fetching recent transactions
    transactions, _ = get_contract_transactions()
    if transactions:
        print(f"Found {len(transactions)} existing transactions.")
        for tx in transactions:
            tx_id = tx.get("txID")
            if tx_id not in processed_txids:  # Skip if already processed
                print(f"\nProcessing existing transaction: {tx_id}")
                transaction_data = fetch_transaction_details(tx_id)
                if transaction_data:
                    await post_transaction_details(page, transaction_data, tx_id)
            else:
                print(f"Transaction ID {tx_id} already processed. Skipping.")
    else:
        print("No existing transactions found.")

# Main function to monitor transactions and post new ones
async def monitor_contract_and_post(page):
    seen_tx_ids = set(load_processed_txids())  # Initialize with already processed txids
    latest_timestamp = None

    print("Monitoring for new transactions...")
    while True:
        transactions, _ = get_contract_transactions(start_timestamp=latest_timestamp)
        for tx in transactions:
            tx_id = tx.get("txID")
            block_timestamp = tx.get("block_timestamp")
            if tx_id and block_timestamp and tx_id not in seen_tx_ids:
                seen_tx_ids.add(tx_id)  # Track new transactions to avoid duplicates
                print(f"\nNew transaction detected: {tx_id} | Timestamp: {block_timestamp}")
                transaction_data = fetch_transaction_details(tx_id)
                if transaction_data:
                    await post_transaction_details(page, transaction_data, tx_id)
                latest_timestamp = block_timestamp  # Update the latest timestamp
        time.sleep(10)

# Main browser launch and login process
async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        page = await browser.new_page()

        await page.goto("https://x.com/login")
        print("Please sign in manually...")
        await page.wait_for_url("https://x.com/home", timeout=0)

        print(f"Logged in. Navigating to profile: {username}...")
        await page.goto(f"https://x.com/{username}")
        await page.wait_for_timeout(3000)

        # Process existing transactions first
        await process_existing_transactions(page)

        # Start monitoring for new transactions
        await monitor_contract_and_post(page)

# Run the script
asyncio.get_event_loop().run_until_complete(main())
