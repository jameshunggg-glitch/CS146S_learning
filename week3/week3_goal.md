# weather-map-server

## 1. Project Overview

### 1.1 Project Goal
- Build a local MCP weather server using Open-Meteo APIs.
- The server should support:
  - searching locations by place name
  - retrieving structured weather forecast data by coordinates
- The goal is to satisfy Week 3 assignment requirements while also practicing:
  - MCP server design
  - tool/interface design
  - AI-readable specifications
  - validation and reliability handling

### 1.2 Why This Project
- Weather data is easy to understand and test.
- Open-Meteo is free to use for learning and does not require API key setup.
- The task is small enough for practice but complete enough to reflect a real MCP workflow.

### 1.3 Scope

#### In Scope
- Local STDIO MCP server
- 2 MCP tools
- Input validation
- Error handling
- Logging
- README and usage instructions

#### Out of Scope
- Remote deployment
- Authentication / OAuth
- Persistent storage
- Caching
- Marine forecast
- Frontend UI

---

## 2. Assignment Alignment

### 2.1 Week 3 Requirements Covered
- External API integration
- At least 2 MCP tools
- Reliability and basic error handling
- Documentation and runnable setup
- Local MCP server deployment mode

### 2.2 What This Project Demonstrates
- MCP fundamentals
- Tool schema design
- Small workflow design
- Clean developer experience
- Structured response formatting

---

## 3. Deployment Mode

### 3.1 Chosen Mode
- Local STDIO MCP server

### 3.2 Why This Mode
- Simpler than remote HTTP deployment
- Easier to debug
- Keeps focus on MCP and tool design
- Best fit for a first practice project

### 3.3 Future Upgrade Options
- HTTP transport
- Remote deployment
- Authenticated endpoints
- Extended tool set

---

## 4. Core Workflow

### 4.1 User-Level Workflow
1. User asks for a location
2. `search_location` returns candidate places
3. User/client selects one result
4. `get_weather_forecast` is called with coordinates
5. Server returns structured current + daily forecast

### 4.2 MCP Workflow
- Client discovers tools
- Client sends tool call
- Server validates inputs
- Server requests Open-Meteo API
- Server formats response
- Server returns structured result or error

---

## 5. Tool Design

### 5.1 Tool 1: `search_location`

#### Purpose
- Search locations by place name and return candidate results.

#### Input Schema
- `query` (string, required)
- `count` (integer, optional, default: 5)
- `language` (string, optional, default: "en")

#### Output Design
- Original query
- List of matched locations
- Result count

#### Example Output Fields
- `name`
- `country`
- `admin1`
- `latitude`
- `longitude`
- `timezone`

#### Validation Rules
- query cannot be empty
- count must be positive and limited to a reasonable range
- language should be a supported string

#### Error Cases
- empty query
- invalid count
- timeout
- API unavailable
- no results found

#### TODO
- Define input schema
- Implement validation
- Connect Geocoding API
- Format response
- Handle empty results
- Add logging

### 5.2 Tool 2: `get_weather_forecast`

#### Purpose
- Retrieve current weather and daily forecast using coordinates.

#### Input Schema
- `latitude` (float, required)
- `longitude` (float, required)
- `timezone` (string, optional, default: "auto")
- `forecast_days` (integer, optional, default: 3)
- `temperature_unit` (string, optional, default: "celsius")
- `wind_speed_unit` (string, optional, default: "kmh")

#### Output Design
- location metadata
- current weather
- daily forecast array

#### Example Output Fields

##### location
- `latitude`
- `longitude`
- `timezone`

##### current
- `time`
- `temperature`
- `wind_speed`
- `weather_code`

##### daily_forecast
- `date`
- `temp_max`
- `temp_min`
- `precipitation_probability`

#### Validation Rules
- latitude must be between -90 and 90
- longitude must be between -180 and 180
- forecast_days must be within an allowed range
- units must be supported values

#### Error Cases
- invalid coordinates
- invalid forecast_days
- timeout
- malformed API response
- empty forecast data

#### TODO
- Define input schema
- Implement validation
- Connect Forecast API
- Extract current weather
- Extract daily weather
- Format response
- Add logging
- Handle API failures

---

## 6. Response and Error Strategy

### 6.1 Success Response Pattern
- `status: "ok"`
- `data: {...}`

### 6.2 Error Response Pattern
- `status: "error"`
- `error_type`
- `message`

### 6.3 Error Types
- `validation_error`
- `timeout_error`
- `api_error`
- `not_found`
- `unexpected_error`

### 6.4 Design Principle
- Keep outputs structured
- Avoid returning raw API payloads directly
- Use predictable response patterns across tools

---

## 7. Reliability Plan

### 7.1 Validation
- Validate all user inputs before API calls

### 7.2 Timeout Handling
- Add request timeout to all external calls

### 7.3 Empty Result Handling
- Return clear "not found" or empty-result messages

### 7.4 API Failure Handling
- Catch HTTP/network exceptions
- Return user-friendly error messages

### 7.5 Rate Limit Awareness
- Even if Open-Meteo is beginner-friendly, note that external APIs may still fail or throttle
- Mention this in README and error handling philosophy

### 7.6 Logging
- Log tool name
- Log input summary
- Log success/failure
- Log error details for debugging

---

## 8. Project Structure

```text
week3/
├── README.md
├── requirements.txt
├── .env.example
├── server.py
├── tools/
│   ├── __init__.py
│   ├── geocoding.py
│   └── weather.py
├── utils/
│   ├── __init__.py
│   ├── http_client.py
│   ├── validators.py
│   └── formatters.py
└── tests/
    ├── test_validators.py
    └── test_formatters.py
```

### 8.1 File Responsibilities
- `server.py`: MCP server entrypoint and tool registration
- `tools/geocoding.py`: location search logic
- `tools/weather.py`: weather forecast logic
- `utils/http_client.py`: shared HTTP request helper
- `utils/validators.py`: input validation
- `utils/formatters.py`: response formatting
- `tests/`: basic tests for reusable logic

---

## 9. Implementation Plan

### Phase 1: Finalize Specs

#### Goals
- Confirm project name
- Confirm tool names
- Confirm schemas
- Confirm response format

#### Deliverables
- final tool specs
- agreed folder structure
- agreed validation rules

### Phase 2: Build MCP Skeleton

#### Goals
- Initialize local MCP server
- Register both tools
- Make server discoverable by client

#### Deliverables
- runnable server skeleton
- empty or mocked tool handlers

### Phase 3: Implement `search_location`

#### Goals
- validate input
- connect geocoding API
- return formatted results

#### Deliverables
- working location search tool

### Phase 4: Implement `get_weather_forecast`

#### Goals
- validate coordinates
- connect forecast API
- combine current + daily forecast

#### Deliverables
- working weather forecast tool

### Phase 5: Improve Reliability

#### Goals
- add timeout
- add error handling
- add logging
- refine error messages

#### Deliverables
- stable tool behavior
- consistent failure responses

### Phase 6: Documentation and Submission

#### Goals
- complete README
- add setup instructions
- add client configuration instructions
- add tool reference and examples

#### Deliverables
- submission-ready project folder

---

## 10. README Plan

### 10.1 Overview
- What the project does
- Why this API was chosen

### 10.2 Features
- `search_location`
- `get_weather_forecast`

### 10.3 Requirements
- Python version
- dependencies

### 10.4 Installation
- create venv
- install packages

### 10.5 Run Instructions
- how to start the server

### 10.6 Client Configuration
- how to connect from Claude Desktop or other MCP client

### 10.7 Tool Reference

#### search_location
- purpose
- inputs
- outputs
- examples

#### get_weather_forecast
- purpose
- inputs
- outputs
- examples

### 10.8 Reliability Notes
- validation
- timeout
- error handling
- limitations

### 10.9 Future Improvements
- split forecast into separate current/daily tools
- add marine forecast
- support remote deployment

---

## 11. Learning Goals

### 11.1 Technical Goals
- Understand MCP server basics
- Learn how to design tool schemas
- Learn how to integrate external APIs
- Practice validation and error handling

### 11.2 Conceptual Goals
- Practice writing AI-readable tool specifications
- Practice workflow thinking
- Practice designing reusable tool interfaces

---

## 12. Future Extensions
- Add `get_current_weather` as a separate tool
- Add `get_daily_forecast` as a separate tool
- Add marine weather forecast
- Add remote HTTP deployment
- Add frontend visualization
- Add caching layer
