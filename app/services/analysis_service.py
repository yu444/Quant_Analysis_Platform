from app.models.stock import Stock, StockMetrics
from app import db

def calculate_metrics(symbol):
    stock = Stock.query.filter_by(symbol=symbol).first()
    if not stock:
        return False

    # This is a simplified example. In a real scenario, you'd perform more complex calculations.
    latest_price = stock.prices.order_by(StockPrice.date.desc()).first()
    
    metrics = StockMetrics(
        stock_id=stock.id,
        date=latest_price.date,
        pe_ratio=stock.info.get('trailingPE'),
        eps=stock.info.get('trailingEps'),
        pb_ratio=stock.info.get('priceToBook'),
        roe=stock.info.get('returnOnEquity'),
        profit_margin=stock.info.get('profitMargins'),
        revenue_growth=stock.info.get('revenueGrowth')
    )
    
    db.session.add(metrics)
    db.session.commit()
    return True
