from app import create_app
from app.services.update_market_index import update_market_indices

app = create_app()
with app.app_context():
    update_market_indices()