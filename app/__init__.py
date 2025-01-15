from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
from flask_session import Session
from config import Config
import pymysql
pymysql.install_as_MySQLdb()

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    #CORS(app, supports_credentials=True, origins=["http://localhost:3000"])
    
    # Disable CORS completely
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    app.config.update(
        SESSION_COOKIE_SAMESITE=None,
        SESSION_COOKIE_SECURE=False,  # Set to True in production with HTTPS
        SESSION_COOKIE_HTTPONLY=False,  # Temporarily for debugging
        REMEMBER_COOKIE_SAMESITE=None
    )
    
    app.config.from_object(config_class)
    
    # Initialize extensions
    Session(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.session_protection = None  # Try this temporarily
    
    # Configure CORS - Single configuration
    CORS(app, 
         resources={
             r"/*": {
                 "origins": ["http://localhost:3000"],
                 "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                 "allow_headers": ["Content-Type", "Authorization"],
                 "supports_credentials": True
             }
         })
    
    @login_manager.user_loader
    def load_user(user_id):
        print(f"Loading user: {user_id}")  # Debug print
        try:
            return User.query.get(int(user_id))
        except Exception as e:
            print(f"Error loading user: {repr(e)}")
            return None

    # Register blueprints
    from app.routes import auth, stock, admin
    app.register_blueprint(auth.bp)
    app.register_blueprint(stock.bp)
    app.register_blueprint(admin.bp)
    
    # Remove the duplicate CORS headers - we'll let Flask-CORS handle it
    # Only add headers that Flask-CORS doesn't handle
    @app.after_request
    def after_request(response):
        # Don't add headers for static resources
        if not request.path.startswith('/static'):
            # Add security headers
            response.headers.add('X-Content-Type-Options', 'nosniff')
            response.headers.add('X-Frame-Options', 'SAMEORIGIN')
            response.headers.add('X-XSS-Protection', '1; mode=block')
        return response
    
    return app

# Import models after app creation
from app import models
from app.models.user import User