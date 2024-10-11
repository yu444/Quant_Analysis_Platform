from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app import db

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register():
    data = request.json
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@bp.route('/login', methods=['POST'])
def login():
    print("login start")
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        login_user(user)
        return jsonify({'message': 'Logged in successfully'}), 200
    return jsonify({'message': 'Invalid username or password'}), 401

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

@bp.route('/check_auth')
def check_auth():
    print("check auth" + str(current_user.is_authenticated))
    if current_user.is_authenticated:
        return jsonify({'message': f'Authenticated'})
    return jsonify({'message': 'Not authenticated'}), 401

@bp.route('/user')
@login_required
def get_user_data():
    print('User accessing /user route')
    print(f'Is authenticated: {current_user.is_authenticated}')
    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        'email': current_user.email,
        # Add any other user data you want to include
        # For example:
        # 'created_at': current_user.created_at.isoformat(),
        # 'last_login': current_user.last_login.isoformat() if current_user.last_login else None,
    }), 200