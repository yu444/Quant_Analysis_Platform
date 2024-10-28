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
    app.config.from_object(config_class)
    
    # Initialize extensions
    Session(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
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
        return User.query.get(int(user_id))

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