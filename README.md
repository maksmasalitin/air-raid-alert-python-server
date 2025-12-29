Server to provide the API for the air raid alerts. All information is taken from https://t.me/air_alert_ua telegram channel.

## Installation

clone the repo
```bash
git clone git@github.com:maksmasalitin/air-raid-alert-python-server.git
cd air-raid-alert-python-server
```
create virtual environment
```bash
python3 -m venv env
source env/bin/activate
````
install dependencies
```bash
pip3 install -r requirements.txt
```

## Configuration

1.  **Obtain Telegram Credentials:**
    *   Go to https://my.telegram.org and log in.
    *   Click on "API development tools".
    *   Create a new application to get your `App api_id` and `App api_hash`.

2.  **Setup Environment:**
    *   Copy the example environment file:
        ```bash
        cp .env.example .env
        ```
    *   Edit `.env` and fill in the values:
        *   `TELEGRAM_API_ID`: Your App `api_id`.
        *   `TELEGRAM_API_HASH`: Your App `api_hash`.
        *   `AUTH_KEYS`: A comma-separated list of secret tokens (e.g., `mysecretkey1,securetoken2`). Clients must send one of these keys to authenticate with the WebSocket server.

## First Run (Session Setup)

Before running the server, you must authenticate with Telegram to generate a session file.

Run the setup script:
```bash
python3 scripts/setup_session.py
```
Follow the interactive prompts to enter your phone number and the verification code sent to your Telegram account. This will create a `telegram-session.session` file in the project root.

## Health Check

To verify that your configuration is correct and the Telegram session is valid without starting the full server:

```bash
python3 scripts/check_status.py
```
If successful, this will print the last alert message from the `@air_alert_ua` channel.

## Usage

Run the server:

```bash
python3 run.py
```

## API

The server implements websocket protocol. https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/Writing_WebSocket_servers

You can connect to the server and receive the air raid alerts in real time. To authourize you need to send the token that configured in .env file. Right after handshake you need to send the token as the first message.
After this server will send you an array with all region ids where the air raid alert is active.

See cient example in examples folder.
