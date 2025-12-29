# Capability: Telegram Integration

## Requirements

### Requirement: Source Monitoring
The system SHALL monitor the official `@air_alert_ua` channel.

#### Scenario: New Message Handling
- **WHEN** a new message event occurs in the channel
- **THEN** the system passes the message to the `AirRaidAlertMessageParser`
- **AND** updates the alert state based on the result

### Requirement: State Initialization
The system SHALL rebuild the current state of alerts upon startup.

#### Scenario: Fetching History
- **WHEN** the Telegram client connects
- **THEN** it iterates through all configured regions
- **AND** searches for the last message containing the region's `#center_region` tag
- **AND** sets the initial alert status based on that message
