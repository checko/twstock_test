from typing import Optional, List
from datetime import date
from sqlmodel import Field, SQLModel, create_engine, Session, select

# Define the Model
class StockPrice(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    stock_id: str = Field(index=True)
    date: date
    open: float
    high: float
    low: float
    close: float
    volume: int

    # Composite unique constraint to prevent duplicate data for same stock/day
    # Note: SQLModel doesn't support composite unique constraints in the class definition easily 
    # without __table_args__, but for simplicity we will handle duplicates in the save logic 
    # or add it if strictly needed. For now, we'll rely on application logic to avoid duplicates.

# Database Setup
sqlite_file_name = "data/stock_data.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# check_same_thread=False is needed for SQLite with multiple threads (like Streamlit + Scheduler)
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def init_db():
    """Creates the database and tables."""
    SQLModel.metadata.create_all(engine)

def save_prices(prices: List[StockPrice]):
    """Saves a list of stock prices to the database."""
    with Session(engine) as session:
        for price in prices:
            # Check if exists to avoid duplicates
            statement = select(StockPrice).where(
                StockPrice.stock_id == price.stock_id,
                StockPrice.date == price.date
            )
            existing = session.exec(statement).first()
            if not existing:
                session.add(price)
        session.commit()

def get_prices(stock_id: str, limit: int = 30) -> List[StockPrice]:
    """Retrieves recent prices for a stock."""
    with Session(engine, expire_on_commit=False) as session:
        statement = select(StockPrice).where(StockPrice.stock_id == stock_id).order_by(StockPrice.date.desc()).limit(limit)
        results = session.exec(statement).all()
        return results
