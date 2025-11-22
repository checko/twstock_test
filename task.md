# Task List: Taiwan Stock Data Collector

## Phase 1: Initialization & Planning
- [x] Define Requirements and Specs <!-- id: 0 -->
- [x] Initialize Git Repository <!-- id: 1 -->
- [x] Create Implementation Plan <!-- id: 2 -->

## Phase 2: Core Infrastructure (Docker & Database)
- [x] Create `Dockerfile` and `docker-compose.yml` <!-- id: 3 -->
- [x] Implement Database Models (`src/database.py`) <!-- id: 4 -->
- [x] Verify Database Creation and Persistence <!-- id: 5 -->

## Phase 3: Data Collection Engine
- [x] Implement TWSE/TPEX Fetcher (`src/fetcher.py`) <!-- id: 6 -->
- [x] Implement Scheduler (`src/scheduler.py`) <!-- id: 7 -->
- [x] Verify Data Fetching and Storage <!-- id: 8 -->

## Phase 4: Web Interface (Streamlit)
- [x] Create Basic Dashboard Layout (`src/main.py`) <!-- id: 9 -->
- [x] Implement "Rising 3 Days" Analysis Logic <!-- id: 10 -->
- [x] Connect UI to Database Query Engine <!-- id: 11 -->
- [x] Verify UI Functionality <!-- id: 12 -->

## Phase 5: Deployment & Documentation
- [ ] Finalize Documentation (Setup Guide) <!-- id: 13 -->
- [ ] Verify Full Docker Deployment on Windows <!-- id: 14 -->
