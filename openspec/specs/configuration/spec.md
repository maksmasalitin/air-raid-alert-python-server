# Capability: Configuration & Parsing

## Requirements

### Requirement: Region Mapping
The system SHALL load region definitions from YAML files in `regions_keywords/`.

#### Scenario: Region Loading
- **WHEN** the parser initializes
- **THEN** it loads all `.yaml` files
- **AND** maps keywords to Region IDs (2-25)
- **AND** identifies the "Center Region" tag for each ID

### Requirement: Alert Logic
The system SHALL determine alert status based on specific text patterns.

#### Scenario: Air Raid Start
- **WHEN** the message contains "Повітряна тривога"
- **THEN** it is classified as an Alert Start

#### Scenario: Air Raid End
- **WHEN** the message contains NOT "Повітряна тривога" (implicitly "Відбій")
- **THEN** it is classified as an Alert End

### Requirement: Center Region Filtering
The system SHALL filter alerts to avoid duplicates for the same region using the `#center_region` tag.

#### Scenario: Center Tag Match
- **WHEN** a message contains the hashtag defined as `center_region` for Region X
- **THEN** the parser returns Region ID X (valid update)

#### Scenario: Non-Center Tag Match
- **WHEN** a message contains a hashtag for Region X but it is NOT the `center_region` tag
- **THEN** the parser returns `IGNORED`
- **AND** the system takes no action (avoids duplicate triggers for sub-districts)
