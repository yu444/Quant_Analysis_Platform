from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from flask_cors import CORS

from flask_session import Session

import pymysql
pymysql.install_as_MySQLdb()

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    app.config['SECRET_KEY'] = 'qap-!@#-123-HJ,'  # Make sure this is set
    app.config['SESSION_TYPE'] = 'filesystem'
    #app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # or however long you want
    Session(app)
    
    # Initialize CORS
    CORS(app, supports_credentials=True)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes import auth, stock, admin
    print("Registering auth blueprint...")
    app.register_blueprint(auth.bp)
    app.register_blueprint(stock.bp)
    app.register_blueprint(admin.bp)
    
    return app

from app import models  # Import models here to ensure they are loaded