import pytest
from datetime import date
from sqlmodel import Session, SQLModel, create_engine
from src.database import StockPrice, save_prices, get_prices

# Use an in-memory SQLite database for testing
@pytest.fixture(name="engine")
def fixture_engine():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    return engine

@pytest.fixture(name="patch_engine")
def fixture_patch_engine(engine, monkeypatch):
    # Patch the engine in src.database to use our test in-memory engine
    monkeypatch.setattr("src.database.engine", engine)
    return engine

def test_save_and_get_prices(patch_engine):
    # Create dummy data
    price1 = StockPrice(
        stock_id="2330",
        date=date(2023, 1, 1),
        open=500.0,
        high=510.0,
        low=495.0,
        close=505.0,
        volume=1000
    )
    
    # Save
    save_prices([price1])
    
    # Retrieve
    results = get_prices("2330")
    assert len(results) == 1
    assert results[0].stock_id == "2330"
    assert results[0].close == 505.0

def test_duplicate_prevention(patch_engine):
    price1 = StockPrice(
        stock_id="2330",
        date=date(2023, 1, 1),
        open=500.0, high=510.0, low=495.0, close=505.0, volume=1000
    )
    
    # Save twice
    save_prices([price1])
    # Create a new instance with same data for the second save
    price2 = StockPrice(
        stock_id="2330",
        date=date(2023, 1, 1),
        open=500.0, high=510.0, low=495.0, close=505.0, volume=1000
    )
    save_prices([price2])
    
    # Should still be 1
    results = get_prices("2330")
    assert len(results) == 1
