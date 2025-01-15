# app/services/update_market_index.py

import sys
import os

from sqlalchemy.dialects.mysql import insert

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
    """Update or insert a market index using MySQL's INSERT ... ON DUPLICATE KEY UPDATE"""
    try:
        # Prepare the data
        data = {
            'name': name,
            'date': date,
            'open_value': float(open_value),
            'high_value': float(high_value),
            'low_value': float(low_value),
            'close_value': float(close_value),
            'volume': int(volume)
        }

        # Create the insert statement
        stmt = insert(MarketIndex).values(**data)
        
        # Add ON DUPLICATE KEY UPDATE clause
        update_dict = {
            'open_value': stmt.inserted.open_value,
            'high_value': stmt.inserted.high_value,
            'low_value': stmt.inserted.low_value,
            'close_value': stmt.inserted.close_value,
            'volume': stmt.inserted.volume,
        }
        
        # Execute upsert
        stmt = stmt.on_duplicate_key_update(**update_dict)
        db.session.execute(stmt)
        db.session.commit()
        
        logger.info(f"Successfully upserted market index: {name} on {date}")
        return True

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error upserting market index {name} on {date}: {str(e)}")
        return False

def update_market_indices():
    """Update all specified market indices in the database."""
    logger.info("Starting market indices update")
    success_count = 0
    error_count = 0

    for index in MARKET_INDICES:
        ticker = index["ticker"]
        name = index["name"]
        
        try:
            # Fetch market data for the ticker symbol
            market_data = fetch_market_data(ticker)
            
            if market_data is not None:
                date = market_data.name.date()
                success = update_market_index(
                    name=name,
                    date=date,
                    open_value=market_data['Open'],
                    high_value=market_data['High'],
                    low_value=market_data['Low'],
                    close_value=market_data['Close'],
                    volume=market_data['Volume']
                )
                if success:
                    success_count += 1
                else:
                    error_count += 1
            else:
                logger.warning(f"No data received for {name} ({ticker})")
                error_count += 1
                
        except Exception as e:
            error_count += 1
            logger.error(f"Failed to update {name}: {str(e)}")
            continue

    logger.info(f"Finished updating market indices. Success: {success_count}, Errors: {error_count}")
    
def run_market_index_update():
    """Run the market index update with app context."""
    with current_app.app_context():
        update_market_indices()

if __name__ == "__main__":
    # For testing the script independently
    app = create_app()
    with app.app_context():
        update_market_indices()