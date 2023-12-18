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

Each region has own id. To identify the region id you can use table from here: https://en.wikipedia.org/wiki/Administrative_divisions_of_Ukraine

### 1. Alerts Endpoint (`/alerts`)
Fetch the current alert statuses for regions.

- **Method:** GET
- **URL:** `/alerts`
- **Parameters:**
    - `auth_key` (string): Required. Authentication key.
    - `is_alert` (boolean): Optional. Filter by alert status (`true` or `false`).

#### Example Usage with `curl`:
```bash
curl "http://<SERVER_URL>:<PORT>/alerts?auth_key=<YOUR_AUTH_KEY>&is_alert=true"
```

#### Example of JSON output:
```json
{
  "8": {
    "is_alert": false,
    "message": "🟢 Відбій тривоги",
    "timestamp": "2023-12-18T09:02:06+00:00"
  },
  "10": {
    "is_alert": true,
    "message": "🔴 Тривога",
    "timestamp": "2023-12-18T09:05:30+00:00"
  }
}

```

### 2. Receive alerts by websocket:

Establish a real-time connection to receive alert updates.

- **URL:** `ws://<SERVER_URL>:<PORT>`
- **Query Parameter:**
    - `auth_key` (string): Required. Authentication key for establishing the connection.

#### Example Usage:
To connect to the WebSocket server using `curl`, use the following command:
```bash
curl --include \
     --no-buffer \
     --header "Connection: Upgrade" \
     --header "Upgrade: websocket" \
     --header "Sec-WebSocket-Key: SGVsbG8sIHdvcmxkIQ==" \
     --header "Sec-WebSocket-Version: 13" \
     "http://<SERVER_URL>:<PORT>/socket.io/?EIO=4&transport=websocket&auth_key=<YOUR_AUTH_KEY>"
```
#### Handling WebSocket Events

When a WebSocket event occurs, a message in the following format will be sent to the client:

Event Format:
```json

{
"region_id": 8,
"timestamp": "2023-12-18T09:02:06+00:00",
"event": "air_raid_end"
}

```

#### Description
- region_id (integer): The ID of the region for which the alert status has changed.
- timestamp (string): The timestamp of when the alert status was updated.
- event (string): The type of event, either `air_raid_alert` or `air_raid_end`.

## Additional notes

- It has /ping endpoint to check if server is alive.
- It has autoreconnect for telegram client, e.g. if network connection is lost, it will try to reconnect.
