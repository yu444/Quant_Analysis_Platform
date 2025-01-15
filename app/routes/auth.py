from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app import db

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['POST'])
def login():
    print("Login attempt started")
    try:
        data = request.get_json()
        print(f"Received data for username: {data.get('username')}")
        
        if not data:
            return jsonify({'message': 'No data provided'}), 400
        
        user = User.query.filter_by(username=data.get('username')).first()
        if user and user.check_password(data.get('password')):
            print("Credentials valid, logging in user")
            try:
                # Store user info before login_user
                user_info = {
                    'username': user.username,
                    'email': user.email
                }
                
                login_success = login_user(user)
                if not login_success:
                    print("Login_user failed")
                    return jsonify({'message': 'Login failed'}), 401
                
                print(f"User logged in successfully: {user_info['username']}")
                return jsonify({
                    'message': 'Logged in successfully',
                    'user': user_info
                }), 200
                
            except Exception as login_error:
                print(f"Error during login_user: {type(login_error).__name__}: {str(login_error)}")
                return jsonify({'message': 'Login process failed'}), 500
            
        print("Invalid credentials")
        return jsonify({'message': 'Invalid username or password'}), 401
        
    except Exception as e:
        error_msg = f"Login error: {type(e).__name__}: {str(e)}"
        print(error_msg)
        return jsonify({'message': 'Internal server error'}), 500

@bp.route('/user', methods=['GET'])
@login_required
def get_user():
    try:
        return jsonify({
            'message': 'User data retrieved',
            'user': {
                'username': current_user.username,
                'email': current_user.email
            }
        }), 200
    except Exception as e:
        print(f"Error getting user data: {type(e).__name__}: {str(e)}")
        return jsonify({'message': 'Error retrieving user data'}), 500

@bp.route('/check_auth', methods=['GET'])
def check_auth():
    try:
        if current_user.is_authenticated:
            return jsonify({
                'message': 'Authenticated',
                'user': {
                    'username': current_user.username,
                    'email': current_user.email
                }
            }), 200
        return jsonify({'message': 'Not authenticated'}), 401
    except Exception as e:
        print(f"Auth check error: {type(e).__name__}: {str(e)}")
        return jsonify({'message': 'Error checking authentication'}), 500

@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    try:
        logout_user()
        return jsonify({'message': 'Logged out successfully'}), 200
    except Exception as e:
        print(f"Logout error: {type(e).__name__}: {str(e)}")
        return jsonify({'message': 'Error during logout'}), 500

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
        print(f"Registration error: {type(e).__name__}: {str(e)}")
        return jsonify({'message': 'Registration failed'}), 500

# Add error handler for unauthorized access
@bp.errorhandler(401)
def unauthorized(e):
    return jsonify({'message': 'Unauthorized access'}), 401