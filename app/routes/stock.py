from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.models.stock import Stock, StockPrice, StockMetrics, MarketIndex
from app.services.stock_service import get_stock_data
from app.services.analysis_service import calculate_metrics
import yfinance as yf
from datetime import datetime, timedelta
from sqlalchemy import desc
from app import db

from flask_cors import cross_origin

bp = Blueprint('stock', __name__)

@bp.route('/search', methods=['GET'])
@cross_origin(origins=['http://localhost:3000'], supports_credentials=True)
@login_required
def search_stocks():
    query = request.args.get('q', '')
    stocks = Stock.query.filter(Stock.symbol.like(f'%{query}%') | 
                              Stock.company_name.like(f'%{query}%')).all()
    return jsonify([{'symbol': s.symbol, 'name': s.company_name} for s in stocks])

@bp.route('/stock/<symbol>', methods=['GET'])
@cross_origin(origins=['http://localhost:3000'], supports_credentials=True)
@login_required
def get_stock_info(symbol):
    stock = Stock.query.filter_by(symbol=symbol).first_or_404()
    latest_price = StockPrice.query.filter_by(stock_id=stock.id)\
                                 .order_by(StockPrice.date.desc()).first()
    latest_metrics = StockMetrics.query.filter_by(stock_id=stock.id)\
                                     .order_by(StockMetrics.date.desc()).first()
    
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
@cross_origin(origins=['http://localhost:3000'], supports_credentials=True)
@login_required
def get_historical_data(symbol):
    stock = Stock.query.filter_by(symbol=symbol).first_or_404()
    prices = StockPrice.query.filter_by(stock_id=stock.id)\
                            .order_by(StockPrice.date).all()
    return jsonify([{
        'date': p.date.isoformat(),
        'close': p.close,
        'volume': p.volume
    } for p in prices])

@bp.route('/stock/<symbol>/metrics', methods=['GET'])
@cross_origin(origins=['http://localhost:3000'], supports_credentials=True)
@login_required
def get_stock_metrics(symbol):
    stock = Stock.query.filter_by(symbol=symbol).first_or_404()
    metrics = StockMetrics.query.filter_by(stock_id=stock.id)\
                               .order_by(StockMetrics.date.desc()).first()
    return jsonify({
        'pe_ratio': metrics.pe_ratio,
        'eps': metrics.eps,
        'pb_ratio': metrics.pb_ratio,
        'roe': metrics.roe,
        'profit_margin': metrics.profit_margin,
        'revenue_growth': metrics.revenue_growth
    })

@bp.route('/market-overview', methods=['GET'])
@cross_origin(origins=['http://localhost:3000'], supports_credentials=True)
def get_market_overview():
    """Get market overview with real-time data from Yahoo Finance"""
    indices = {
        'S&P 500': '^GSPC',
        'Dow Jones': '^DJI',
        'NASDAQ': '^IXIC'
    }
    
    market_data = {}
    
    for name, symbol in indices.items():
        index = yf.Ticker(symbol)
        info = index.info
        market_data[name] = {
            'price': info.get('previousClose', 'N/A'),
            'change': info.get('regularMarketChange', 'N/A'),
            'change_percent': info.get('regularMarketChangePercent', 'N/A')
        }
    
    return jsonify(market_data)

@bp.route('/market-indices/latest', methods=['GET'])
@cross_origin(origins=['http://localhost:3000'], supports_credentials=True)
def get_latest_indices():
    """Get latest market indices data from database"""
    try:
        # Get latest date with data
        latest_date = db.session.query(MarketIndex.date)\
                               .order_by(desc(MarketIndex.date))\
                               .first()
        
        if not latest_date:
            return jsonify({'error': 'No index data available'}), 404
            
        latest_date = latest_date[0]
        
        # Get all indices for the latest date
        indices = MarketIndex.query.filter_by(date=latest_date).all()
        
        indices_data = {}
        for index in indices:
            # Get previous day's data for comparison
            prev_day = MarketIndex.query\
                .filter(MarketIndex.name == index.name,
                       MarketIndex.date < latest_date)\
                .order_by(desc(MarketIndex.date))\
                .first()
            
            # Calculate daily change and percentage
            daily_change = None
            change_percent = None
            if prev_day and prev_day.close_value and index.close_value:
                daily_change = index.close_value - prev_day.close_value
                change_percent = (daily_change / prev_day.close_value) * 100
            
            indices_data[index.name] = {
                'name': index.name,
                'date': index.date.isoformat(),
                'latest_value': index.close_value,
                'open': index.open_value,
                'high': index.high_value,
                'low': index.low_value,
                'volume': index.volume,
                'daily_change': daily_change,
                'change_percent': change_percent,
                'daily_range': (index.high_value - index.low_value) if index.high_value and index.low_value else None
            }
        
        return jsonify({
            'date': latest_date.isoformat(),
            'indices': indices_data,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        print(f"Error in get_latest_indices: {str(e)}")
        return jsonify({'error': 'Failed to retrieve market indices data'}), 500

@bp.route('/market-indices/historical/<name>', methods=['GET'])
@cross_origin(origins=['http://localhost:3000'], supports_credentials=True)
def get_index_historical(name):
    """Get historical data for a specific market index"""
    try:
        # Get date range from query parameters
        days = request.args.get('days', 30, type=int)
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        
        # Query historical data
        historical_data = MarketIndex.query\
            .filter(MarketIndex.name == name,
                   MarketIndex.date.between(start_date, end_date))\
            .order_by(MarketIndex.date)\
            .all()
        
        if not historical_data:
            return jsonify({'error': f'No historical data found for index {name}'}), 404
            
        return jsonify({
            'name': name,
            'data': [{
                'date': data.date.isoformat(),
                'open': data.open_value,
                'high': data.high_value,
                'low': data.low_value,
                'close': data.close_value,
                'volume': data.volume,
                'daily_range': (data.high_value - data.low_value) if data.high_value and data.low_value else None
            } for data in historical_data]
        })
        
    except Exception as e:
        print(f"Error in get_index_historical: {str(e)}")
        return jsonify({'error': 'Failed to retrieve historical index data'}), 500

@bp.route('/market-indices/summary', methods=['GET'])
@cross_origin(origins=['http://localhost:3000'], supports_credentials=True)
def get_indices_summary():
    """Get a summary of all market indices with their latest values"""
    try:
        # Get the latest date for each index using a subquery
        latest_dates = db.session.query(
            MarketIndex.name,
            db.func.max(MarketIndex.date).label('max_date')
        ).group_by(MarketIndex.name).subquery()
        
        # Join with the main table to get the latest values
        latest_indices = db.session.query(MarketIndex)\
            .join(latest_dates,
                  db.and_(
                      MarketIndex.name == latest_dates.c.name,
                      MarketIndex.date == latest_dates.c.max_date
                  ))\
            .all()
        
        summary_data = []
        for index in latest_indices:
            # Get previous day's value for change calculation
            prev_day = MarketIndex.query\
                .filter(MarketIndex.name == index.name,
                       MarketIndex.date < index.date)\
                .order_by(desc(MarketIndex.date))\
                .first()
            
            change = None
            change_percent = None
            if prev_day and prev_day.close_value and index.close_value:
                change = index.close_value - prev_day.close_value
                change_percent = (change / prev_day.close_value) * 100
            
            summary_data.append({
                'name': index.name,
                'current_value': index.close_value,
                'change': change,
                'change_percent': change_percent,
                'volume': index.volume,
                'updated_at': index.date.isoformat()
            })
        
        return jsonify({
            'indices': summary_data,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        print(f"Error in get_indices_summary: {str(e)}")
        return jsonify({'error': 'Failed to retrieve indices summary'}), 500