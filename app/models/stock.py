from app import db
from datetime import datetime

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), unique=True, nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    sector = db.Column(db.String(50))
    industry = db.Column(db.String(50))
    
    prices = db.relationship('StockPrice', backref='stock', lazy='dynamic')
    metrics = db.relationship('StockMetrics', backref='stock', lazy='dynamic')

class StockPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    open = db.Column(db.Float, nullable=False)
    high = db.Column(db.Float, nullable=False)
    low = db.Column(db.Float, nullable=False)
    close = db.Column(db.Float, nullable=False)
    volume = db.Column(db.BigInteger, nullable=False)

class StockMetrics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    pe_ratio = db.Column(db.Float)
    eps = db.Column(db.Float)
    pb_ratio = db.Column(db.Float)
    roe = db.Column(db.Float)
    profit_margin = db.Column(db.Float)
    revenue_growth = db.Column(db.Float)
    
class MarketIndex(db.Model):
    __tablename__ = 'market_indices'
    __table_args__ = (
        db.UniqueConstraint('name', 'date', name='uix_market_indices_name_date'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True)
    date = db.Column(db.Date, index=True)
    open_value = db.Column(db.Float)
    high_value = db.Column(db.Float)
    low_value = db.Column(db.Float)
    close_value = db.Column(db.Float)
    volume = db.Column(db.BigInteger)

# Example usage: Create instances for each index
s_and_p_500 = MarketIndex(name="S&P 500", date=datetime.now().date())
dow_30 = MarketIndex(name="Dow 30", date=datetime.now().date())
nasdaq = MarketIndex(name="Nasdaq", date=datetime.now().date())
russell_2000 = MarketIndex(name="Russell 2000", date=datetime.now().date())
crude_oil = MarketIndex(name="Crude Oil", date=datetime.now().date())
gold = MarketIndex(name="Gold", date=datetime.now().date())