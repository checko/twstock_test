from typing import List, Dict
from src.database import StockPrice, get_prices, Session, engine, select

def find_rising_stocks(days: int = 3) -> List[Dict]:
    """
    Finds stocks that have been rising for at least 'days' consecutive days.
    Returns a list of dicts with stock info.
    """
    # This is a naive implementation. For large datasets, do this in SQL or pandas.
    # Since we are using SQLite and might have many stocks, iterating all is slow.
    # Better approach: Get distinct stock_ids, then check each.
    # Or use a complex SQL query.
    
    # For MVP with small watchlist, iterating is fine.
    # We need to know which stocks we have.
    
    rising_stocks = []
    
    with Session(engine) as session:
        # Get all unique stock_ids
        statement = select(StockPrice.stock_id).distinct()
        stock_ids = session.exec(statement).all()
        
        for stock_id in stock_ids:
            # Get last N+1 days to compare
            prices = get_prices(stock_id, limit=days + 1)
            
            if len(prices) < days + 1:
                continue
            
            # Check if rising
            # prices[0] is latest date
            is_rising = True
            for i in range(days):
                # prices[i] should be > prices[i+1] (Today > Yesterday)
                if prices[i].close <= prices[i+1].close:
                    is_rising = False
                    break
            
            if is_rising:
                rising_stocks.append({
                    "stock_id": stock_id,
                    "latest_price": prices[0].close,
                    "date": prices[0].date
                })
                
    return rising_stocks
