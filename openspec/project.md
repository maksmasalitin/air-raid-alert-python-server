# Project Context

## Purpose
A lightweight asynchronous WebSocket server that provides real-time air raid alert statuses for Ukraine, specifically designed for MicroPython clients. It sources data from the Telegram channel `@air_alert_ua`.

## Tech Stack
- **Language:** Python 3.10+ (standard `asyncio`)
- **WebSocket:** `websockets` library (RFC 6455)
- **Telegram Client:** Telethon (Async)
- **Configuration:** `python-dotenv`

## Project Conventions

### Code Style
- **Python:** PEP 8.
- **Async:** Consistent use of `async`/`await` throughout the core logic.
- **Naming:** CamelCase for classes, snake_case for functions and variables.

### Architecture Patterns
- **Entry Point:** `run.py` uses `asyncio.run()` to start the application.
- **Asynchronous Tasks:** The Telegram client and WebSocket server run as concurrent `asyncio` tasks.
- **State Management:** In-memory `Country` model stores the current state of alert regions (IDs 2-25).
- **Event Driven:** Telegram `NewMessage` events trigger state updates and immediate broadcasts to all connected WebSocket clients.
- **Initialization:** On startup, the server fetches the last message for each region to populate the initial state.

### Testing Strategy
- *Currently undefined (no test suite present).*

### Git Workflow
- Development occurs on specialized branches (e.g., `web_socket_for_micropython_client`).

## Domain Context
- **Regions:** Identified by integer IDs (2 to 25).
- **Alert Source:** The official `@air_alert_ua` Telegram channel.
- **MicroPython Compatibility:** The server uses a simple post-handshake authentication message to keep the client-side implementation minimal.

## Important Constraints
- **Authentication:** Clients MUST send the `AUTH_KEY` as the first message after the WebSocket handshake. Failure to do so or an invalid key results in immediate connection closure.
- **Single Channel Source:** The system is tightly coupled to the message format of the `@air_alert_ua` channel.

## External Dependencies
- **Telegram API:** Required for real-time alert monitoring.