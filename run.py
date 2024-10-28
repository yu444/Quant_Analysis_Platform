from app import create_app, db
from flask_migrate import Migrate
from config import Config  # Add this import

app = create_app(Config)  # Pass Config class explicitly
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True)