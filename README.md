# Taiwan Stock Data Collector

A self-hosted web application designed to automatically collect daily trading data for Taiwan stocks (TWSE/TPEX) and provide tools for technical analysis, such as identifying stocks with specific price trends.

Designed to run on a **Raspberry Pi 4B** using **Docker**, with a **Streamlit** web interface for easy interaction.

## Documentation

For detailed information about the project's goals and technical architecture, please refer to the following documents:

*   **[Requirements Document](requirements.md)**: Functional goals, user stories, and hardware requirements.
*   **[Technical Specifications](specs.md)**: System architecture, database schema, and technology stack.

## Quick Start

### Option 1: Run with Docker (Recommended for RPi)
1.  Ensure Docker and Docker Compose are installed.
2.  Run the application:
    ```bash
    docker-compose up -d --build
    ```
3.  Open your browser to `http://localhost:8501` (or your RPi's IP).

### Option 2: Run Locally (Development)
1.  Install `uv` (if not installed):
    ```powershell
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```
2.  Install dependencies:
    ```bash
    uv pip install -r requirements.txt
    ```
3.  Run the app:
    ```bash
    uv run streamlit run src/main.py
    ```

## Features
*   **Daily Automation**: Fetches data automatically at 14:30 (Asia/Taipei).
*   **Trend Analysis**: Find stocks rising for N consecutive days.
*   **Resilient**: Retries on failure, stores data in SQLite.

