import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
from src.fetcher import fetch_daily_data
from src.database import StockPrice

# Mock data structure returned by twstock
class MockStockData:
    def __init__(self, date, open, high, low, close, capacity):
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.capacity = capacity

@patch("src.fetcher.twstock.Stock")
@patch("src.fetcher.save_prices")
def test_fetch_daily_data(mock_save_prices, mock_stock_class):
    # Setup Mock
    mock_stock_instance = MagicMock()
    mock_stock_class.return_value = mock_stock_instance
    
    # Mock return data
    mock_data = [
        MockStockData(
            date=datetime(2023, 1, 1),
            open=100.0, high=105.0, low=99.0, close=102.0, capacity=10000
        )
    ]
    mock_stock_instance.fetch_31.return_value = mock_data
    
    # Run function
    fetch_daily_data(["2330"])
    
    # Verify
    mock_stock_class.assert_called_with("2330")
    mock_stock_instance.fetch_31.assert_called_once()
    
    # Verify save_prices was called
    assert mock_save_prices.call_count == 1
    saved_list = mock_save_prices.call_args[0][0]
    assert len(saved_list) == 1
    assert isinstance(saved_list[0], StockPrice)
    assert saved_list[0].stock_id == "2330"
    assert saved_list[0].close == 102.0
