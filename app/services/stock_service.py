import yfinance as yf
from app.models.stock import Stock, StockPrice
from app import db

def get_stock_data(symbol):
    stock = yf.Ticker(symbol)
    info = stock.info
    history = stock.history(period="1y")

    db_stock = Stock.query.filter_by(symbol=symbol).first()
    if not db_stock:
        db_stock = Stock(symbol=symbol, company_name=info['longName'], 
                         sector=info.get('sector'), industry=info.get('industry'))
        db.session.add(db_stock)
    
    for date, row in history.iterrows():
        price = StockPrice(stock_id=db_stock.id, date=date.date(), 
                           open=row['Open'], high=row['High'], 
                           low=row['Low'], close=row['Close'], 
                           volume=row['Volume'])
        db.session.add(price)
    
    db.session.commit()
    return True

def update_stock_data(symbol):
    return get_stock_data(symbol)
