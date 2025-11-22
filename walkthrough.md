# Walkthrough: Taiwan Stock Data Collector

I have successfully built the **Taiwan Stock Data Collector** application. It is designed to run on your Raspberry Pi (via Docker) or your Windows machine.

## What has been built?
1.  **Database Layer (`src/database.py`)**:
    *   Uses **SQLModel** (SQLite) to store stock prices.
    *   Handles data persistence in `data/stock_data.db`.
2.  **Data Fetcher (`src/fetcher.py`)**:
    *   Uses `twstock` library to fetch daily data.
    *   Includes retry logic and rate limiting.
3.  **Scheduler (`src/scheduler.py`)**:
    *   Runs automatically every day at **14:30** (Asia/Taipei).
4.  **Web Interface (`src/main.py`)**:
    *   **Streamlit** dashboard to view status and analyze trends.
    *   **"Rising 3 Days"** feature implemented in `src/analysis.py`.

## Verification Results
I have verified the core logic with automated unit tests:
*   **Database**: Verified saving/loading and duplicate prevention.
*   **Fetcher**: Verified integration with `twstock` (mocked).
*   **Analysis**: Verified the algorithm to detect rising stocks.

## How to Run

### On Windows (Development)
1.  Open terminal in project folder.
2.  Run: `uv run streamlit run src/main.py`
3.  Click **"Update Data Now"** to fetch initial data.
4.  Go to **"Analysis"** tab to find rising stocks.

### On Raspberry Pi (Production)
1.  Copy the project folder to RPi.
2.  Run: `docker-compose up -d --build`
3.  The app will start and run automatically.

## Next Steps
*   Deploy to your Raspberry Pi.
*   Add more stocks to the `WATCHLIST` in `src/scheduler.py` (or make it editable in the UI).
