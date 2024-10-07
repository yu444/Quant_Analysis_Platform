from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.models.user import User
from app.services.stock_service import update_stock_data
from app import db

bp = Blueprint('admin', __name__)

@bp.route('/admin/update_stock/<symbol>', methods=['POST'])
@login_required
def admin_update_stock(symbol):
    user = User.query.filter_by(id=current_user.id).first()
    if not user.is_admin:
        return jsonify({'message': 'Unauthorized'}), 403
    
    success = update_stock_data(symbol)
    if success:
        return jsonify({'message': f'Stock data for {symbol} updated successfully'}), 200
    else:
        return jsonify({'message': 'Failed to update stock data'}), 500
