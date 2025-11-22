import pytest
from datetime import date, timedelta
from src.analysis import find_rising_stocks
from src.database import StockPrice, save_prices, init_db, engine
from sqlmodel import Session, SQLModel, create_engine

# Use in-memory DB for testing
@pytest.fixture(name="patch_engine_analysis")
def fixture_patch_engine_analysis(monkeypatch):
    test_engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(test_engine)
    monkeypatch.setattr("src.analysis.engine", test_engine)
    monkeypatch.setattr("src.database.engine", test_engine)
    return test_engine

def test_find_rising_stocks(patch_engine_analysis):
    # Create data: Stock A rising for 3 days
    # Dates: Today, Yesterday, DayBefore
    today = date.today()
    d1 = today
    d2 = today - timedelta(days=1)
    d3 = today - timedelta(days=2)
    d4 = today - timedelta(days=3)
    
    prices = [
        # Stock A: Rising (100 -> 101 -> 102 -> 103)
        StockPrice(stock_id="A", date=d1, close=103.0, open=0, high=0, low=0, volume=0),
        StockPrice(stock_id="A", date=d2, close=102.0, open=0, high=0, low=0, volume=0),
        StockPrice(stock_id="A", date=d3, close=101.0, open=0, high=0, low=0, volume=0),
        StockPrice(stock_id="A", date=d4, close=100.0, open=0, high=0, low=0, volume=0),
        
        # Stock B: Falling (100 -> 99 -> 98)
        StockPrice(stock_id="B", date=d1, close=98.0, open=0, high=0, low=0, volume=0),
        StockPrice(stock_id="B", date=d2, close=99.0, open=0, high=0, low=0, volume=0),
        StockPrice(stock_id="B", date=d3, close=100.0, open=0, high=0, low=0, volume=0),
    ]
    
    save_prices(prices)
    
    # Test
    results = find_rising_stocks(days=3)
    
    assert len(results) == 1
    assert results[0]["stock_id"] == "A"
    assert results[0]["latest_price"] == 103.0

def test_not_enough_data(patch_engine_analysis):
    prices = [
        StockPrice(stock_id="C", date=date.today(), close=100.0, open=0, high=0, low=0, volume=0)
    ]
    save_prices(prices)
    results = find_rising_stocks(days=3)
    assert len(results) == 0
