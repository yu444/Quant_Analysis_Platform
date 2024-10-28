class Config:
    # Basic Flask Configuration
    SECRET_KEY = 'qap-!@#-123-HJ,'
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://itp211:itp211@localhost/quant_analysis_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session Configuration
    SESSION_TYPE = 'filesystem'
    
    # CORS Configuration
    CORS_HEADERS = 'Content-Type'
    
    # Debug mode
    DEBUG = True