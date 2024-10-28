from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app import db

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'No data provided'}), 400
            
        user = User.query.filter_by(username=data.get('username')).first()
        if user and user.check_password(data.get('password')):
            login_user(user)
            return jsonify({
                'message': 'Logged in successfully',
                'user': {
                    'username': user.username,
                    'email': user.email
                }
            }), 200
            
        return jsonify({'message': 'Invalid username or password'}), 401
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({'message': 'Login failed'}), 500

@bp.route('/check_auth', methods=['GET'])
def check_auth():
    if current_user.is_authenticated:
        return jsonify({
            'message': 'Authenticated',
            'user': {
                'username': current_user.username,
                'email': current_user.email
            }
        })
    return jsonify({'message': 'Not authenticated'}), 401

@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'})

@bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'No data provided'}), 400

        # Check if user exists
        if User.query.filter_by(username=data.get('username')).first():
            return jsonify({'message': 'Username already exists'}), 409
            
        if User.query.filter_by(email=data.get('email')).first():
            return jsonify({'message': 'Email already registered'}), 409

        user = User(username=data['username'], email=data['email'])
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Registration error: {str(e)}")
        return jsonify({'message': 'Registration failed'}), 500