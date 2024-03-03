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

## Usage

setup environment variables using ENV variables or .env file:
```bash
cp .env.example .env
```
run the server

```bash
python3 run.py
```

Telegram will ask you to enter your phone number and then the code that you will receive. After that you will be able to use the API.

## API

The server implements websocket protocol. https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/Writing_WebSocket_servers

You can connect to the server and receive the air raid alerts in real time. To authourize you need to send the token that configured in .env file. Right after handshake you need to send the token as the first message.
After this server will send you an array with all region ids where the air raid alert is active.

See cient example in examples folder.
