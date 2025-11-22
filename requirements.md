# Requirements Document: Taiwan Stock Data Collector & Analyzer

## 1. Project Overview
A self-hosted web application designed to automatically collect daily trading data for Taiwan stocks, store it locally, and provide an interface for querying specific market trends (e.g., "prices rising for 3 consecutive days").

## 2. Target Environment
*   **Production Server**: Raspberry Pi 4B (Linux).
*   **Development Environment**: Windows 10/11.
*   **Deployment Method**: Docker (Containerized for consistency across Windows and RPi).

## 3. Functional Requirements

### 3.1 Data Collection
*   **Source**: Taiwan Stock Exchange (TWSE) and Taipei Exchange (TPEX).
*   **Frequency**: Automatic daily execution (e.g., 2:00 PM or after market close).
*   **Scope**: Ability to track all listed stocks or a user-defined watchlist.
*   **Resilience**: System must handle network failures and retry data fetching.

### 3.2 Data Storage
*   **Database**: SQLite.
    *   *Reasoning*: Lightweight, serverless, single-file storage makes it extremely easy to backup or migrate to another machine.
*   **Retention**: Historical data should be kept indefinitely for trend analysis.

### 3.3 Data Analysis & Querying
*   **Core Query**: Identify stocks with specific price patterns.
    *   *Primary Use Case*: "List stocks where the closing price has risen for 3 consecutive days."
*   **Extensibility**: The system should allow adding new analysis strategies (e.g., Moving Average Crossovers, RSI) in the future.

### 3.4 User Interface
*   **Type**: Web-based Dashboard (Local Network).
*   **Features**:
    *   **Status Panel**: Show when data was last updated and if the daily job succeeded.
    *   **Manual Trigger**: Button to force a data update immediately.
    *   **Analysis View**: Input parameters (e.g., "Rising Days: 3") and view a table/chart of matching stocks.

## 4. Non-Functional Requirements
*   **Performance**: Must run smoothly on low-power hardware (Raspberry Pi 4B).
*   **Portability**: The entire system (code + database) must be easily movable to a new machine.
*   **Maintainability**: Code should be modular (separation of data fetching, storage, and UI).
