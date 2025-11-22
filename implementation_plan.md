# Implementation Plan - Taiwan Stock Data Collector

# Goal Description
Build a Dockerized Python application to collect daily Taiwan stock data, store it in SQLite, and provide a Streamlit web interface for analyzing trends (specifically "Rising 3 Days").

## User Review Required
> [!IMPORTANT]
> **Docker Dependency**: This plan assumes Docker Desktop is installed and running on the Windows development machine.
> **Data Source**: We rely on the `twstock` library which fetches from public TWSE/TPEX APIs. Excessive requests might lead to temporary IP bans; we will implement rate limiting/delays.

## Local Development Tooling
- **Package Manager**: `uv` (User preference for Windows dev).
- **Command**: Use `uv venv` to create environment and `uv pip install -r requirements.txt` (or `uv add`) to manage dependencies.

## Proposed Changes & Execution Order

### Step 1: Core Infrastructure (Database)
#### [NEW] [src/database.py](file:///d:/koko/project/twstock/src/database.py)
- Defines `StockPrice` model using SQLModel.
- Handles SQLite connection (`sqlite:///data/stock_data.db`).
- Provides helper functions: `init_db()`, `save_prices()`, `get_prices()`.

#### [NEW] [tests/test_database.py](file:///d:/koko/project/twstock/tests/test_database.py)
- Unit tests for DB creation, saving, and retrieving data.

#### [VERIFY] Test Database
- Run `uv run pytest tests/test_database.py`
- **STOP**: Ensure DB tests pass before proceeding.

### Step 2: Data Collection Engine
#### [NEW] [src/fetcher.py](file:///d:/koko/project/twstock/src/fetcher.py)
- `fetch_daily_data()`: Uses `twstock` to get data.
- Handles retries and error logging.

#### [NEW] [tests/test_fetcher.py](file:///d:/koko/project/twstock/tests/test_fetcher.py)
- Mock `twstock` to verify data parsing logic without hitting real API.

#### [VERIFY] Test Fetcher
- Run `uv run pytest tests/test_fetcher.py`
- **STOP**: Ensure Fetcher tests pass before proceeding.

### Step 3: Scheduler & Integration
#### [NEW] [src/scheduler.py](file:///d:/koko/project/twstock/src/scheduler.py)
- Uses `APScheduler` to run `fetch_daily_data()` daily at 14:30.

#### [NEW] [Dockerfile](file:///d:/koko/project/twstock/Dockerfile)
- Python 3.10-slim base image.
- Installs dependencies.

#### [NEW] [docker-compose.yml](file:///d:/koko/project/twstock/docker-compose.yml)
- Defines services.

### Step 4: User Interface
#### [NEW] [src/main.py](file:///d:/koko/project/twstock/src/main.py)
- Streamlit entry point.
- Sidebar: Status, Manual Update Button.
- Main Area: "Analysis" tab.
- Logic to query DB for "Rising 3 Days" and display as a DataFrame.

## Verification Plan

### Automated Tests
- Run full suite: `uv run pytest`

### Manual Verification
1.  **Build**: Run `docker-compose up --build`.
2.  **UI Check**: Open `http://localhost:8501`.
3.  **Trigger**: Click "Update Data Now" and verify logs show successful fetch.
4.  **Persistence**: Restart container and verify data is still visible in the UI.
