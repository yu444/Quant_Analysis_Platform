# manage_schedule.py
from flask_apscheduler import APScheduler
from app import create_app
from app.services.update_market_index import update_market_indices
import logging
from datetime import datetime

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = create_app()
scheduler = APScheduler()

# Wrapper function to provide app context
def run_update_with_context():
    with app.app_context():
        update_market_indices()

def init_scheduler():
    # Basic scheduler config
    scheduler.init_app(app)
    
    # Schedule the job with the wrapper function
    scheduler.add_job(
        id='market_update',
        func=run_update_with_context,  # Use wrapper instead of direct function
        trigger='interval',
        minutes=1
    )
    
    scheduler.start()
    print(f"Scheduler started at {datetime.now()}")
    print("Market indices will update every minute")
    print("Press Ctrl+C to stop")

if __name__ == "__main__":
    with app.app_context():
        init_scheduler()
        app.run(debug=False, use_reloader=False)