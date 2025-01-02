# app/services/update_market_index.py

import sys
import os

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

import yfinance as yf
import pandas as pd
from sqlalchemy.exc import IntegrityError
import logging
from flask import current_app
from app import db, create_app
from app.models.stock import MarketIndex  # Ensure this path matches your project structure

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# List of market indices to update
MARKET_INDICES = [
    {"name": "S&P 500", "ticker": "^GSPC"},
    {"name": "Dow 30", "ticker": "^DJI"},
    {"name": "Nasdaq", "ticker": "^IXIC"},
    {"name": "Russell 2000", "ticker": "^RUT"},
    {"name": "Crude Oil", "ticker": "CL=F"},
    {"name": "Gold", "ticker": "GC=F"}
]

def fetch_market_data(ticker):
    """Fetch market data for a given ticker symbol."""
    try:
        data = yf.download(ticker, period='1d')  # Fetch data for the last day
        return data.iloc[-1]  # Get the most recent row of data
    except Exception as e:
        logger.error(f"Error fetching market data for {ticker}: {e}")
        return None

def update_market_index(name, date, open_value, high_value, low_value, close_value, volume):
    """Update or insert a market index in the database."""
    try:
        # Use get() instead of first() to ensure we get None if not found
        index_record = MarketIndex.query.filter_by(name=name, date=date).first()
        
        if index_record:
            # Update existing record
            index_record.open_value = open_value
            index_record.high_value = high_value
            index_record.low_value = low_value
            index_record.close_value = close_value
            index_record.volume = volume
            logger.info(f"Updated market index: {name} on {date}")
        else:
            # Create new record
            index_record = MarketIndex(
                name=name,
                date=date,
                open_value=open_value,
                high_value=high_value,
                low_value=low_value,
                close_value=close_value,
                volume=volume
            )
            db.session.add(index_record)
            logger.info(f"Inserted new market index: {name} on {date}")
        
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        # Try to update if record exists (in case of race condition)
        try:
            db.session.query(MarketIndex).filter_by(name=name, date=date).update({
                'open_value': open_value,
                'high_value': high_value,
                'low_value': low_value,
                'close_value': close_value,
                'volume': volume
            })
            db.session.commit()
            logger.info(f"Updated existing market index after integrity error: {name} on {date}")
        except Exception as inner_e:
            db.session.rollback()
            logger.error(f"Error updating market index {name} on {date} after integrity error: {inner_e}")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating market index {name} on {date}: {e}")
def update_market_indices():
    """Update all specified market indices in the database."""
    print("--------------------------------------")  # Clear visual separator
    #print(f"Running update_market_indices at: {datetime.now()}")  # Add timestamp
    logger.info("update_market_indices started")
    for index in MARKET_INDICES:
        ticker = index["ticker"]
        name = index["name"]
        
        # Fetch market data for the ticker symbol
        market_data = fetch_market_data(ticker)
        
        if market_data is not None:
            date = market_data.name.date()  # Get the date from the DataFrame index
            open_value = market_data['Open']
            high_value = market_data['High']
            low_value = market_data['Low']
            close_value = market_data['Close']
            volume = market_data['Volume']
            
            update_market_index(name, date, open_value, high_value, low_value, close_value, volume)
    
    logger.info("Finished updating market indices")

def run_market_index_update():
    """Run the market index update with app context."""
    with current_app.app_context():
        update_market_indices()

if __name__ == "__main__":
    # For testing the script independently
    app = create_app()
    with app.app_context():
        update_market_indices()