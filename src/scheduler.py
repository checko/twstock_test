from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import time
from src.fetcher import fetch_daily_data

# List of stocks to track (Example list, can be moved to config or DB)
WATCHLIST = ["2330", "2317", "2454", "2308"] # TSMC, Hon Hai, MediaTek, Delta

def start_scheduler():
    """Starts the background scheduler."""
    scheduler = BackgroundScheduler()
    
    # Schedule job to run every day at 14:30 (2:30 PM)
    # Taiwan Stock Market closes at 13:30, data usually available by 14:30
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
    print("Scheduler started. Job 'daily_fetch' scheduled for 14:30 Asia/Taipei.")
    
    # Keep the main thread alive if running standalone
    try:
        while True:
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

if __name__ == "__main__":
    start_scheduler()
