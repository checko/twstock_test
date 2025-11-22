import twstock
import time
from datetime import datetime, date
from typing import List, Optional
from src.database import StockPrice, save_prices

def fetch_daily_data(stock_ids: List[str]) -> None:
    """
    Fetches daily data for the given stock IDs and saves to DB.
    Handles retries and rate limiting.
    """
    print(f"Starting fetch for {len(stock_ids)} stocks...")
    
    for stock_id in stock_ids:
        try:
            print(f"Fetching {stock_id}...")
            stock = twstock.Stock(stock_id)
            
            # Get recent data (last 31 days to ensure we cover enough for analysis)
            # twstock.fetch_31() returns data for the last 31 days
            data = stock.fetch_31()
            
            prices_to_save = []
            for entry in data:
                # entry is a namedtuple or object with date, open, high, low, close, capacity, etc.
                # twstock returns date as datetime object
                
                # Check if data is valid (sometimes it returns None or empty)
                if not entry.date:
                    continue

                price = StockPrice(
                    stock_id=stock_id,
                    date=entry.date.date(),
                    open=entry.open,
                    high=entry.high,
                    low=entry.low,
                    close=entry.close,
                    volume=int(entry.capacity) # capacity is volume (shares)
                )
                prices_to_save.append(price)
            
            if prices_to_save:
                save_prices(prices_to_save)
                print(f"Saved {len(prices_to_save)} records for {stock_id}")
            
            # Rate limiting to avoid ban
            time.sleep(3) 
            
        except Exception as e:
            print(f"Error fetching {stock_id}: {e}")
            # Continue to next stock even if one fails
            continue
