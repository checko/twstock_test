# Technical Specifications: Taiwan Stock Data Collector

## 1. Architecture Overview
The application follows a monolithic architecture within a Docker container, consisting of three main components:
1.  **Scheduler**: Triggers data fetching jobs.
2.  **Data Engine**: Handles API requests to TWSE/TPEX and database operations.
3.  **Web Interface**: Provides user interaction and visualization.

## 2. Technology Stack

| Component | Technology | Justification |
| :--- | :--- | :--- |
| **Language** | Python 3.10+ | Rich ecosystem for finance (`twstock`, `pandas`) and rapid web dev. |
| **Web Framework** | Streamlit | Extremely fast to build interactive data dashboards without writing HTML/CSS. |
| **Database** | SQLite | Zero-configuration, single-file database (`stock_data.db`). Ideal for RPi. |
| **ORM** | SQLModel (or SQLAlchemy) | Simplifies database interactions and schema management. |
| **Containerization** | Docker | Ensures identical environment on Windows Dev and RPi Prod. |
| **Stock Library** | `twstock` | Specialized library for Taiwan stock data. |

## 3. Database Schema
**Table: `daily_prices`**
*   `id` (PK): Composite or Auto-increment
*   `stock_id`: String (e.g., "2330")
*   `date`: Date (YYYY-MM-DD)
*   `open`: Float
*   `high`: Float
*   `low`: Float
*   `close`: Float
*   `volume`: Integer

## 4. Application Structure
```
/twstock-app
├── data/
│   └── stock_data.db      # Persisted volume (mounted from host)
├── src/
│   ├── main.py            # Streamlit entry point
│   ├── fetcher.py         # Logic to download data from twstock
│   ├── database.py        # DB connection and models
│   └── scheduler.py       # Background job runner (APScheduler)
├── Dockerfile             # Container definition
├── docker-compose.yml     # Deployment config
└── requirements.txt       # Python dependencies
```

## 5. Deployment Strategy (Docker)
The application will be packaged as a single Docker image.
*   **Volume Mapping**: A host directory (e.g., `./data`) will be mounted to `/app/data` inside the container to ensure `stock_data.db` persists across container restarts.
*   **Restart Policy**: `restart: always` to ensure the service comes back up after a power cycle on the Raspberry Pi.

## 6. Development Workflow
1.  **Local (Windows)**:
    *   Code in VS Code.
    *   Run locally via `streamlit run src/main.py` OR `docker-compose up`.
2.  **Deploy (RPi)**:
    *   Push code to Git.
    *   Pull on RPi.
    *   Run `docker-compose up -d --build`.
