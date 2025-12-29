# Capability: WebSocket Server

## Requirements

### Requirement: Client Authentication
The server SHALL require immediate authentication upon connection.

#### Scenario: Successful Auth
- **WHEN** a client connects
- **AND** sends an `AUTH_KEY` present in the server configuration as the first message
- **THEN** the server accepts the connection
- **AND** sends the current alert state (JSON list of region IDs)

#### Scenario: Failed Auth
- **WHEN** a client connects
- **AND** sends an invalid key
- **THEN** the server sends `{"error": "Authentication failed"}`
- **AND** closes the connection

### Requirement: State Broadcasting
The server SHALL push state updates to all connected clients immediately upon change.

#### Scenario: Alert Update
- **WHEN** the internal alert state changes
- **THEN** the server iterates through all `connected_clients`
- **AND** sends the new state (JSON list of region IDs) to each
