import streamlit as st
import pandas as pd
from src.database import init_db
from src.scheduler import start_scheduler
from src.fetcher import fetch_daily_data, WATCHLIST
from src.analysis import find_rising_stocks
import threading

# Page Config
st.set_page_config(page_title="TW Stock Collector", layout="wide")

# Initialize DB
init_db()

# Start Scheduler (Singleton)
@st.cache_resource
def init_scheduler():
    # Run scheduler in a separate thread to not block Streamlit
    # Actually start_scheduler() in scheduler.py blocks if we don't run it in background.
    # But BackgroundScheduler is background.
    # The start_scheduler function in src/scheduler.py has a while True loop.
    # We should modify src/scheduler.py or just use the scheduler object directly here.
    # Let's just import the scheduler class and start it.
    from apscheduler.schedulers.background import BackgroundScheduler
    from apscheduler.triggers.cron import CronTrigger
    
    scheduler = BackgroundScheduler()
    trigger = CronTrigger(hour=14, minute=30, timezone="Asia/Taipei")
    scheduler.add_job(
        fetch_daily_data,
        trigger=trigger,
        args=[WATCHLIST],
        id="daily_fetch",
        name="Daily Stock Fetch",
        replace_existing=True
    )
    scheduler.start()
    return scheduler

scheduler = init_scheduler()

# Sidebar
st.sidebar.title("Control Panel")
st.sidebar.write(f"Scheduler Running: {scheduler.running}")

if st.sidebar.button("Update Data Now"):
    with st.spinner("Fetching data..."):
        fetch_daily_data(WATCHLIST)
    st.success("Data updated!")

# Main Content
st.title("Taiwan Stock Data Collector")

tab1, tab2 = st.tabs(["Analysis", "Raw Data"])

with tab1:
    st.header("Trend Analysis")
    days = st.number_input("Consecutive Rising Days", min_value=1, value=3)
    
    if st.button("Find Rising Stocks"):
        results = find_rising_stocks(days)
        if results:
            df = pd.DataFrame(results)
            st.dataframe(df)
        else:
            st.info("No stocks found matching criteria.")

with tab2:
    st.header("Database View")
    # Show some raw data
    # We need a function to get all data or recent data
    # For now just show nothing or implement a viewer later
    st.write("Raw data view coming soon.")
