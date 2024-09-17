# **XLG NFT BUY BOT - Transaction Monitoring and Posting Bot Documentation**

## **Table of Contents**

1. [Introduction](#introduction)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Installation Guide](#installation-guide)
    - [1. Clone the Repository](#1-clone-the-repository)
    - [2. Set Up the Python Environment](#2-set-up-the-python-environment)
    - [3. Install Dependencies](#3-install-dependencies)
    - [4. Install Playwright Browsers](#4-install-playwright-browsers)
5. [Configuration](#configuration)
    - [1. Environment Variables](#1-environment-variables)
    - [2. Configuration File (Optional)](#2-configuration-file-optional)
6. [Usage Guide](#usage-guide)
    - [1. Running the Script](#1-running-the-script)
    - [2. Manual Transaction Processing](#2-manual-transaction-processing)
    - [3. Monitoring New Transactions](#3-monitoring-new-transactions)
7. [Development Documentation](#development-documentation)
    - [1. Code Structure Overview](#1-code-structure-overview)
    - [2. Detailed Function Descriptions](#2-detailed-function-descriptions)
    - [3. Extending Functionality](#3-extending-functionality)
    - [4. Best Practices for Maintenance](#4-best-practices-for-maintenance)
8. [Security Considerations](#security-considerations)
9. [Troubleshooting](#troubleshooting)
10. [FAQs](#faqs)
11. [Support Information](#support-information)
12. [Appendix](#appendix)
    - [1. Dependency List](#1-dependency-list)

---

## **Introduction**

Welcome to the **Transaction Monitoring and Posting Bot** documentation. This script is designed to monitor transactions on the Tron blockchain for a specific contract (`$XLG`) and a particular deck (`TDuEK3tqCn9YPFNAFd7SDypdqDisNXm1xr`). Upon detecting relevant transactions, the bot processes the transaction details and posts them automatically to a specified profile on [X.com](https://x.com) (formerly known as Twitter).

This documentation provides comprehensive guidance for both end-users and developers to effectively install, configure, use, and maintain the bot.

---

## **Features**

- **Transaction Monitoring:** Continuously monitors transactions related to a specific Tron contract and deck.
- **Data Processing:** Extracts and formats relevant transaction details, including buyer/seller addresses, transaction amounts, and token IDs.
- **Automated Posting:** Uses Playwright to automate browser interactions and post transaction details to X.com.
- **Image Attachment:** Attaches relevant images based on token IDs if available.
- **Transaction Tracking:** Maintains a record of processed transactions to prevent duplicate postings.
- **Manual Transaction Processing:** Allows manual addition and processing of specific transaction IDs.

---

## **Prerequisites**

Before installing and running the bot, ensure your system meets the following requirements:

- **Operating System:** 
  - Windows 10 or later
  - macOS 10.15 (Catalina) or later
  - Linux (Ubuntu 20.04 LTS or later recommended)
  
- **Python:** 
  - Version 3.8 or higher

- **Internet Connection:** 
  - Stable internet connection for API interactions and browser automation.

- **Hardware Requirements:**
  - Minimum 2 GB RAM
  - Sufficient storage for images and transaction logs

---

## **Installation Guide**

Follow these steps to set up the Transaction Monitoring and Posting Bot on your system.

### **1. Clone the Repository**

Clone the repository containing the script to your local machine.

```bash
git clone https://github.com/cybershrapnel/xlgnftbuybot.git
cd xlgnftbuybot
```

### **2. Set Up the Python Environment**

It's recommended to use a virtual environment to manage dependencies but not necessary.

#### **Using `venv`:**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **3. Install Dependencies**

Install the required Python packages using `pip`.

```bash
pip install -r requirements.txt
```

### **4. Install Playwright Browsers**

Playwright requires browser binaries to function correctly.

```bash
playwright install
```

*This command will download and install the necessary browsers (Chromium, Firefox, WebKit).*

---

## **Configuration**

Proper configuration is crucial for the bot to function as intended. The bot uses environment variables for configuration, ensuring sensitive information is not hard-coded.

### **1. Environment Variables**

Set the following environment variables to configure the bot: (Values are preconfigured no adjustments needed, just for reference)

- **`XLG_CONTRACT_ADDRESS`**
  - **Description:** Contract address for `$XLG`.
  - **Default:** `TQr5axvJzETeHsUiXv6QjBEh1BKH571AZu`
  
- **`USERNAME`**
  - **Description:** Your username on X.com where the bot will post transactions.
  - **Default:** `xlgnftbuybot`
  
- **`SPECIFIC_DECK_ADDRESS`**
  - **Description:** Specific contract address for the deck to filter transactions.
  - **Default:** `TDuEK3tqCn9YPFNAFd7SDypdqDisNXm1xr`
  
- **`IMAGES_FOLDER`**
  - **Description:** Directory where images are stored.
  - **Default:** `images`
  
- **`TXIDS_FILE`**
  - **Description:** Path to the `txids.txt` file that stores processed transaction IDs.
  - **Default:** `txids.txt`
  
- **`TRONGRID_API_URL`**
  - **Description:** TronGrid API endpoint.
  - **Default:** `https://api.trongrid.io/v1/contracts/{}/transactions`
  
- **`TRONSCAN_API_URL`**
  - **Description:** TronScan API endpoint for transaction details.
  - **Default:** `https://apilist.tronscanapi.com/api/transaction-info?hash={}`

---

## **Usage Guide**

This section provides step-by-step instructions on how to use the Transaction Monitoring and Posting Bot effectively.

Make sure to unzip the images folder and that the txids.txt filfe is up to date with what any other instance of the bot may have posted on another server such as from the development server.

All images should be directly in the images folder and the txt file should be in the same directory as the py script.

download and unzip the images from the files on the release page. They were too big to upload.

Download from https://github.com/cybershrapnel/xlgnftbuybot/releases/tag/images

### **1. Running the Script**

To start the bot, execute the main script using Python.

```bash
python transaction_monitoring_bot.py
```

*Ensure that your virtual environment is activated and all dependencies are installed.*

Once the script starts a firefox web browser will load and will wait for you to login to X with the proper user that the script is configured for.
Once you login in the script will do everything on it's own.

### **2. Manual Transaction Processing**

The bot allows manual addition and processing of specific transaction IDs. This is useful for reprocessing or handling transactions not detected automatically or for adding older transactions from the past.
Make sure any manual additions are not in the txids.txt file or they will be ignored.

1. **Add Transaction IDs:**

   Open the `transaction_monitoring_bot.py` script and locate the `process_existing_transactions` function. Under the `# Manually add the transaction ID to process` section, add any transaction IDs you wish to process.

   ```python
   transaction_ids = ["0c943af20dec1668fca83c9cb35b2b5ebd094db09a41796e865e2a11765008d8", "another_tx_id_here"]
   ```

2. **Run the Script:**

   Execute the script as usual. The bot will process the manually added transaction IDs if they haven't been processed before.

### **3. Monitoring New Transactions**

After processing existing transactions, the bot enters a monitoring loop to detect and handle new transactions in real-time.

- **Automatic Detection:** The bot polls the TronGrid API every 10 seconds to check for new transactions related to the specified contract and deck.
- **Processing New Transactions:** Upon detecting a new transaction, the bot fetches its details, formats the information, attaches relevant images (if available), and posts the details to the configured X.com profile.
- **Transaction Tracking:** Processed transaction IDs are saved to `txids.txt` to prevent duplicate postings.

*The monitoring process continues indefinitely until the script is terminated.*

** Note that image 107 and 1076 were not accessible via BTFS. I did not include placeholders and you may want to find the correct images or add placeholders.
It should function fine and post with no image but there is a chance it could crash as I did not test those two cases.
---

## **Development Documentation**

This section provides an in-depth overview of the script's architecture, key functions, and guidelines for extending or maintaining the bot.

### **1. Code Structure Overview**

The script is organized into several key components:

- **Imports and Dependencies:**
  - Standard libraries: `os`, `time`, `hashlib`, etc.
  - Third-party libraries: `requests`, `base58`, `playwright`, `asyncio`
  
- **Configuration Variables:**
  - Defines contract addresses, usernames, file paths, and API endpoints.
  
- **Utility Functions:**
  - `load_processed_txids()`: Loads already processed transaction IDs.
  - `save_processed_txid(tx_id)`: Saves a new transaction ID to avoid reprocessing.
  - `get_contract_transactions()`: Fetches transactions related to the specified contract.
  - `fetch_transaction_details(tx_id)`: Retrieves detailed information about a transaction.
  - `hex_to_base58(hex_address)`: Converts Ethereum-style hex addresses to Tron base58 addresses.
  - `format_transaction_summary(transaction_data, tx_id)`: Formats transaction details by switching buyer and seller.
  - `format_transfer_details(transaction_data)`: Extracts and formats transfer details, including token IDs.
  - `type_text(page, selector, value)`: Simulates typing into a contenteditable div.
  - `get_trx_spent_on_transaction(tx_id)`: Calculates the total TRX spent in a transaction.
  - `attach_image_if_exists(page, token_id)`: Attaches an image based on the token ID if available.
  - `post_transaction_details(page, transaction_data, tx_id)`: Orchestrates the process of posting transaction details to X.com.
  
- **Main Workflow Functions:**
  - `process_existing_transactions(page)`: Processes existing transactions, including manually added ones.
  - `monitor_contract_and_post(page)`: Continuously monitors for new transactions and posts them.
  - `main()`: Initializes Playwright, handles login, navigates to the user profile, and starts processing and monitoring transactions.
  
- **Script Execution:**
  - The script is executed asynchronously using `asyncio.get_event_loop().run_until_complete(main())`.

### **2. Detailed Function Descriptions**

#### **Utility Functions**

- **`load_processed_txids()`**
  - **Purpose:** Reads the `txids.txt` file and loads processed transaction IDs into a set.
  - **Returns:** A set of transaction IDs (`Set[str]`).
  
- **`save_processed_txid(tx_id)`**
  - **Purpose:** Appends a new transaction ID to the `txids.txt` file to mark it as processed.
  - **Parameters:** 
    - `tx_id` (`str`): The transaction ID to save.
  
- **`get_contract_transactions(limit=200, start_timestamp=None)`**
  - **Purpose:** Fetches a list of transactions related to the specified contract from TronGrid API.
  - **Parameters:** 
    - `limit` (`int`): Number of transactions to fetch (default: 200).
    - `start_timestamp` (`int` or `None`): Optional timestamp to filter transactions.
  - **Returns:** A tuple containing a list of transactions and an optional error message.
  
- **`fetch_transaction_details(tx_id)`**
  - **Purpose:** Retrieves detailed information about a specific transaction using TronGrid API.
  - **Parameters:** 
    - `tx_id` (`str`): The transaction ID to fetch details for.
  - **Returns:** A JSON object containing transaction details or `None` if failed.
  
- **`hex_to_base58(hex_address)`**
  - **Purpose:** Converts an Ethereum-style hexadecimal address to a Tron base58 address.
  - **Parameters:** 
    - `hex_address` (`str`): The hexadecimal address to convert.
  - **Returns:** A base58 encoded Tron address (`str`).
  
- **`format_transaction_summary(transaction_data, tx_id)`**
  - **Purpose:** Formats the transaction summary by switching buyer and seller labels.
  - **Parameters:** 
    - `transaction_data` (`dict`): The transaction data fetched from the API.
    - `tx_id` (`str`): The transaction ID.
  - **Returns:** A formatted string containing transaction details or `None`.
  
- **`format_transfer_details(transaction_data)`**
  - **Purpose:** Extracts and formats transfer details, including the token ID.
  - **Parameters:** 
    - `transaction_data` (`dict`): The transaction data fetched from the API.
  - **Returns:** A tuple containing formatted transfer details (`str`) and the token ID (`str` or `None`).
  
- **`type_text(page, selector, value)`**
  - **Purpose:** Simulates typing text into a contenteditable div on a web page using Playwright.
  - **Parameters:** 
    - `page`: The Playwright page object.
    - `selector` (`str`): The CSS selector for the target element.
    - `value` (`str`): The text to type.
  
- **`get_trx_spent_on_transaction(tx_id)`**
  - **Purpose:** Calculates the total TRX spent in a specific transaction using TronScan API.
  - **Parameters:** 
    - `tx_id` (`str`): The transaction ID.
  - **Returns:** The total TRX spent (`float`) or `None` if not found.
  
- **`attach_image_if_exists(page, token_id)`**
  - **Purpose:** Attaches an image to the post if an image corresponding to the token ID exists.
  - **Parameters:** 
    - `page`: The Playwright page object.
    - `token_id` (`str` or `None`): The token ID to find the corresponding image.
  
- **`post_transaction_details(page, transaction_data, tx_id)`**
  - **Purpose:** Coordinates the process of formatting transaction details and posting them to X.com.
  - **Parameters:** 
    - `page`: The Playwright page object.
    - `transaction_data` (`dict`): The transaction data fetched from the API.
    - `tx_id` (`str`): The transaction ID.

#### **Main Workflow Functions**

- **`process_existing_transactions(page)`**
  - **Purpose:** Processes existing transactions, including manually added transaction IDs and those fetched from the API.
  - **Parameters:** 
    - `page`: The Playwright page object.
  
- **`monitor_contract_and_post(page)`**
  - **Purpose:** Continuously monitors for new transactions and processes them as they are detected.
  - **Parameters:** 
    - `page`: The Playwright page object.

- **`main()`**
  - **Purpose:** Initializes Playwright, handles the login process, navigates to the user profile, and starts processing and monitoring transactions.
  - **Parameters:** None

### **3. Extending Functionality**

To enhance or customize the bot further, consider the following guidelines:

- **Adding Support for Multiple Decks:**
  - Modify the `SPECIFIC_DECK_ADDRESS` to accept multiple addresses.
  - Update filtering logic to handle multiple decks.
  
- **Enhancing Error Handling:**
  - Implement retry mechanisms for API requests.
  - Integrate advanced logging (e.g., logging to a file or external service).
  
- **Improving Image Handling:**
  - Support multiple image formats (e.g., PNG, GIF).
  - Implement image caching or validation.
  
- **Integrating with Other Platforms:**
  - Extend the posting functionality to other social media platforms or communication channels.
  
- **User Interface:**
  - Develop a GUI for easier configuration and monitoring.
  
- **Notification System:**
  - Implement email or SMS notifications for successful or failed postings.

### **4. Best Practices for Maintenance**

- **Regular Updates:**
  - Keep dependencies updated to their latest versions to benefit from security patches and new features.
  
- **Code Reviews:**
  - Periodically review and refactor code to improve efficiency and readability.
  
- **Documentation:**
  - Maintain and update this documentation as the script evolves.
  
- **Testing:**
  - Implement unit and integration tests to ensure functionality remains intact during changes.
  
- **Version Control:**
  - Use a version control system (e.g., Git) to track changes and manage different versions of the script.

---

## **Security Considerations**

Ensuring the security of your bot and the data it handles is paramount. Follow these best practices:

- **Secure Storage of Credentials:**
  - Avoid hard-coding sensitive information (e.g., API keys, login credentials) in the script.
  - Use environment variables or secure secrets management services.
  
- **Access Control:**
  - Restrict access to the system where the bot is running.
  - Use strong, unique passwords for all accounts involved.
  
- **Regular Audits:**
  - Periodically review the code for potential security vulnerabilities.
  
- **API Rate Limits:**
  - Be mindful of API rate limits to prevent your IP from being throttled or banned.
  
- **Data Validation:**
  - Validate and sanitize all data fetched from external sources before processing.
  
- **Logging:**
  - Avoid logging sensitive information. Ensure logs do not contain personal or confidential data.

---

## **Troubleshooting**

Encountering issues while setting up or running the bot? Refer to the common problems and their solutions below.

### **1. Playwright Browser Not Launching**

**Problem:** Playwright fails to launch the browser or throws an error related to browser binaries.

**Solution:**
- Ensure that you have installed Playwright browsers by running:
  ```bash
  playwright install
  ```
- Verify that your system meets the requirements for Playwright.
- Check for any firewall or antivirus settings that might be blocking Playwright.

### **2. API Request Failures**

**Problem:** API requests to TronGrid or TronScan are failing with status codes like 429 (Too Many Requests) or 500 (Internal Server Error).

**Solution:**
- **Rate Limiting:** Implement exponential backoff or increase the interval between requests.
- **API Status:** Check the status pages of TronGrid and TronScan to ensure their APIs are operational.
- **Network Issues:** Verify your internet connection and proxy settings.

### **3. Unable to Log In to X.com**

**Problem:** The bot is unable to complete the login process to X.com.

**Solution:**
- **Manual Login:** Ensure you complete the manual login prompt promptly.
- **Two-Factor Authentication:** If X.com uses 2FA, consider disabling it for the bot account or using an automation-friendly method.
- **Selector Changes:** X.com may have updated its UI. Update the CSS selectors in the script accordingly.

### **4. Image Attachment Failures**

**Problem:** The bot fails to attach images even when they exist in the specified folder.

**Solution:**
- **File Path:** Ensure the `IMAGES_FOLDER` path is correct and the images are named using the token IDs (e.g., `token123.jpg`).
- **File Format:** Verify that the images are in the correct format (`.jpg`) or update the script to handle different formats.
- **Permissions:** Check file permissions to ensure the script has access to read the images.

### **5. Duplicate Postings**

**Problem:** The bot posts the same transaction multiple times.

**Solution:**
- **Transaction Tracking:** Ensure that the `txids.txt` file is being updated correctly after each successful post.
- **File Permissions:** Verify that the script has write permissions to `txids.txt`.
- **Concurrent Access:** Avoid running multiple instances of the script simultaneously, which might cause race conditions.

---

## **FAQs**

### **Q1. What is the purpose of this bot?**

**A:** The bot monitors transactions on the Tron blockchain for a specific contract and deck. Upon detecting relevant transactions, it processes and posts the transaction details automatically to a specified X.com profile.

### **Q2. Do I need to have a developer account or API keys?**

**A:** The current version of the script uses public APIs provided by TronGrid and TronScan, which do not require API keys for basic usage. However, for higher request rates or additional features, obtaining API keys from these services might be necessary.

### **Q3. How do I add more transaction IDs to be processed manually?**

**A:** Open the `transaction_monitoring_bot.py` script, locate the `process_existing_transactions` function, and add the desired transaction IDs to the `transaction_ids` list.

### **Q4. Can I change the target platform from X.com to another social media platform?**

**A:** Yes, but it would require modifying the browser automation part of the script. You would need to update the selectors and interaction logic to match the new platform's interface.

### **Q5. How can I ensure the bot runs continuously without interruptions?**

**A:** Consider deploying the bot on a dedicated server or cloud service with high availability. Use process managers like `systemd`, `pm2`, or Docker containers to manage the bot's lifecycle and ensure it restarts automatically in case of failures.
(I can easily set the script up on a loop with auto login features in case of crash or failure but that is not very secure)

---

## **Appendix**

### **1. Dependency List**

Ensure all the following packages are installed. You can install them using `pip` as shown below:

- **Python Standard Libraries:**
  - `os`
  - `time`
  - `hashlib`
  - `asyncio`

- **Third-Party Libraries:**
  - `requests`: For synchronous HTTP requests.
  - `base58`: For encoding addresses.
  - `playwright`: For browser automation.
  - `aiohttp`: For asynchronous HTTP requests (if you upgrade to an async version).
  - `aiofiles`: For asynchronous file operations (if you upgrade to an async version).
  - `python-dotenv` (Optional): For loading environment variables from a `.env` file.

#### **Installation Command:**

```bash
pip install requests base58 playwright aiohttp aiofiles python-dotenv
```

*Note: Ensure `playwright` is properly installed and the browsers are set up using `playwright install`.*

---

# **Conclusion**

This documentation aims to provide a comprehensive guide for setting up, using, and maintaining the Transaction Monitoring and Posting Bot. By following the outlined steps and best practices, you can ensure the bot operates efficiently and securely, effectively fulfilling its purpose of monitoring Tron blockchain transactions and posting relevant details to X.com.

---
