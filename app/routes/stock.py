from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.models.stock import Stock, StockPrice, StockMetrics
from app.services.stock_service import get_stock_data
from app.services.analysis_service import calculate_metrics
import yfinance as yf

bp = Blueprint('stock', __name__)

@bp.route('/search', methods=['GET'])
@login_required
def search_stocks():
    query = request.args.get('q', '')
    stocks = Stock.query.filter(Stock.symbol.like(f'%{query}%') | Stock.company_name.like(f'%{query}%')).all()
    return jsonify([{'symbol': s.symbol, 'name': s.company_name} for s in stocks])

@bp.route('/stock/<symbol>', methods=['GET'])
@login_required
def get_stock_info(symbol):
    stock = Stock.query.filter_by(symbol=symbol).first_or_404()
    latest_price = StockPrice.query.filter_by(stock_id=stock.id).order_by(StockPrice.date.desc()).first()
    latest_metrics = StockMetrics.query.filter_by(stock_id=stock.id).order_by(StockMetrics.date.desc()).first()
    
    return jsonify({
        'symbol': stock.symbol,
        'name': stock.company_name,
        'sector': stock.sector,
        'industry': stock.industry,
        'latest_price': latest_price.close if latest_price else None,
        'pe_ratio': latest_metrics.pe_ratio if latest_metrics else None,
        'eps': latest_metrics.eps if latest_metrics else None
    })

@bp.route('/stock/<symbol>/historical', methods=['GET'])
@login_required
def get_historical_data(symbol):
    stock = Stock.query.filter_by(symbol=symbol).first_or_404()
    prices = StockPrice.query.filter_by(stock_id=stock.id).order_by(StockPrice.date).all()
    return jsonify([{'date': p.date, 'close': p.close, 'volume': p.volume} for p in prices])

@bp.route('/stock/<symbol>/metrics', methods=['GET'])
@login_required
def get_stock_metrics(symbol):
    stock = Stock.query.filter_by(symbol=symbol).first_or_404()
    metrics = StockMetrics.query.filter_by(stock_id=stock.id).order_by(StockMetrics.date.desc()).first()
    return jsonify({
        'pe_ratio': metrics.pe_ratio,
        'eps': metrics.eps,
        'pb_ratio': metrics.pb_ratio,
        'roe': metrics.roe,
        'profit_margin': metrics.profit_margin,
        'revenue_growth': metrics.revenue_growth
    })
    
@bp.route('/market-overview', methods=['GET'])
def get_market_overview():
    print("get_market_overview started")
    # Define major indices
    indices = {
        'S&P 500': '^GSPC',
        'Dow Jones': '^DJI',
        'NASDAQ': '^IXIC'
    }
    
    market_data = {}
    
    for name, symbol in indices.items():
        index = yf.Ticker(symbol)
        info = index.info
        #print(name + " info:" + str(index.info))
        market_data[name] = {
            'price': info.get('previousClose', 'N/A'),
            'change': info.get('regularMarketChange', 'N/A'),
            'change_percent': info.get('regularMarketChangePercent', 'N/A')
        }
        print(name + " :" + str(market_data[name]))
    
    # You can add more market data here, such as:
    # - Top gainers/losers
    # - Sector performance
    # - Market breadth indicators
    
    return jsonify(market_data)
