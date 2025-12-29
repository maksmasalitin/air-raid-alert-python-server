# Capability: System Architecture

## Requirements

### Requirement: Real-time Alert Relay
The system SHALL act as a bridge between Telegram alert channels and WebSocket clients.

#### Scenario: End-to-End Flow
- **WHEN** a new alert message is posted to `@air_alert_ua`
- **THEN** the Telegram Client receives the message
- **AND** the Parser determines the region and status
- **AND** the System updates the internal state
- **AND** the WebSocket Server broadcasts the updated state to all authenticated clients

### Requirement: Async Concurrency
The system SHALL run network-bound components as concurrent asyncio tasks.

#### Scenario: Startup
- **WHEN** the application starts (`run.py`)
- **THEN** it initializes the Telegram Client task
- **AND** it initializes the WebSocket Server task
- **AND** it runs them concurrently in the event loop
