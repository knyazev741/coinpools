# NotCoinBot Pool Notifications

## Description

NotCoinBot Pool Notifications is a project designed to provide instant notifications about new pools in NotCoinBot. This project helps users save time by avoiding unnecessary logins to check for tasks and enables them to earn more in the game by immediately notifying them when new pools are available for earning.

## Installation

### System Requirements

- Python 3.x
- Virtual environment (venv)
- ChromeDriver (for Selenium)

### Steps

1. **Clone the repository**:
    ```sh
    git clone https://github.com/knyazev741/coinpools
    cd coinpools
    ```

2. **Create and activate a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Install ChromeDriver**:

    - **On Ubuntu/Debian**:
        ```sh
        sudo apt-get update
        sudo apt-get install -y chromium-chromedriver
        ```

        Make sure that ChromeDriver is in your PATH. You can verify this by running:
        ```sh
        which chromedriver
        ```

    - **On Fedora**:
        ```sh
        sudo dnf install chromedriver
        ```

    - **On Windows and macOS**:
        Download the ChromeDriver from the [official website](https://sites.google.com/chromium.org/driver/downloads) and ensure the downloaded ChromeDriver executable is in your PATH or specify its path in the `.env` file under `CHROME_DRIVER_PATH`.

## Configuration

Copy the `env.template` file to `.env` and fill in the required parameters. Here is a detailed explanation of each parameter:

```ini
# Account URL with authentication parameters for https://farm.joincommunity.xyz/
# Replace with your personal URL including authentication key and other parameters
URL=

# Account level corresponding to the URL above. Can be Bronze, Silver, Gold, or Platinum
LEVEL=

# Path to the SQLite database file
DB_FILE=

# Path to the ChromeDriver executable
CHROME_DRIVER_PATH=

# Telegram bot token for posting messages to the channel
BOT_TOKEN=

# Telegram channel ID where the bot will post messages
CHANNEL_ID=

# Telegram admin ID to whom the bot will send error messages
ADMIN_ID=
```
### Note on URL

To obtain the `URL` parameter:

1. Open the Telegram Web client at [web.telegram.org](https://web.telegram.org).
2. Log into the account that you will use to get data from NotCoin.
3. Open the NotCoin application in Telegram.
4. Right-click on the NotCoin application and select "Inspect" to open Developer Tools.
5. In Developer Tools, find the `iframe Class zA1w1IOq ` tag that contains the URL for NotCoin. This URL usually includes an authentication key and other parameters.
6. Copy this URL and paste it into the `URL` parameter in your `.env` file.

## Usage

To run the main script, use the following command:

```sh
python3 main.py
```
This will start the process of monitoring pools and sending notifications.

## Testing

To run tests, use the following command:

```sh
python3 test_main.py
```
### What to Expect

	•	A message should be sent to your specified Telegram channel indicating new pools.
	•	A message should be sent to the admin Telegram account indicating “Test: No errors” if the tests run successfully.

### Important Note

Ensure that the bot token specified in the .env file is granted permission to send messages to the admin. The admin must send the /start command to the bot to allow it to send messages. Also, make sure that the bot specified in the configuration is added as an administrator to the channel and has sufficient permissions to send messages.
