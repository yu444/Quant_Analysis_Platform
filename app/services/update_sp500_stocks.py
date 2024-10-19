# app/services/update_sp500_stocks.py

import sys
import os
from datetime import datetime, timedelta

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from app import db, create_app
from app.models.stock import Stock
from app.models.stock import StockPrice  # Ensure this path matches your project structure

import yfinance as yf
import pandas as pd

from sqlalchemy.exc import IntegrityError
import logging
from flask import current_app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_sp500_stocks():
    """Download list of S&P 500 companies"""
    try:
        sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
        return sp500[['Symbol', 'Security', 'GICS Sector', 'GICS Sub-Industry']].values.tolist()
    except Exception as e:
        logger.error(f"Error fetching S&P 500 stocks: {e}")
        return []

def update_stock(symbol, company_name, sector, industry):
    """Update or insert a stock in the database"""
    try:
        stock = Stock.query.filter_by(symbol=symbol).first()
        if stock:
            stock.company_name = company_name
            stock.sector = sector
            stock.industry = industry
        else:
            stock = Stock(symbol=symbol, company_name=company_name, sector=sector, industry=industry)
            db.session.add(stock)
        db.session.commit()
        logger.info(f"Updated/Inserted stock: {symbol}")
    except IntegrityError:
        db.session.rollback()
        logger.error(f"IntegrityError for stock: {symbol}")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating stock {symbol}: {e}")

def fetch_and_update_stock_prices(symbol):
    """Fetch historical prices for a given stock symbol and update the database"""
    try:
        # Fetch historical data for the past year
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        
        # Fetch historical prices using yfinance
        historical_data = yf.download(symbol, start=start_date, end=end_date)

        for date, row in historical_data.iterrows():
            # Create or update StockPrice entries
            price_record = StockPrice.query.filter_by(stock_id=symbol, date=date.date()).first()
            if price_record:
                price_record.open = row['Open']
                price_record.high = row['High']
                price_record.low = row['Low']
                price_record.close = row['Close']
                price_record.volume = row['Volume']
            else:
                # Assuming you have a way to get the stock ID from the symbol
                stock_id = Stock.query.filter_by(symbol=symbol).first().id
                new_price_record = StockPrice(
                    stock_id=stock_id,
                    date=date.date(),
                    open=row['Open'],
                    high=row['High'],
                    low=row['Low'],
                    close=row['Close'],
                    volume=row['Volume']
                )
                db.session.add(new_price_record)

        db.session.commit()
        logger.info(f"Updated prices for stock: {symbol}")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error fetching/updating prices for {symbol}: {e}")

def update_sp500_stocks():
    """Update all S&P 500 stocks in the database"""
    stocks = get_sp500_stocks()
    for symbol, company_name, sector, industry in stocks:
        update_stock(symbol, company_name, sector, industry)
        fetch_and_update_stock_prices(symbol)  # Fetch and update prices after updating stock info
    logger.info("Finished updating S&P 500 stocks")

def run_sp500_update():
    """Run the S&P 500 stock update with app context"""
    with current_app.app_context():
        update_sp500_stocks()

if __name__ == "__main__":
    # For testing the script independently
    app = create_app()
    with app.app_context():
        update_sp500_stocks()