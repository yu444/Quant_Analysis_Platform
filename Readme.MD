# Quant Analysis Platform

Author: Joey Zhang
Date: 2024-Oct-7

Please ensure you are at virtual env by using command:
```bash
venv\Scripts\activate
```

## Project Overview
The Quant Analysis Platform is a web-based application designed to provide quantitative analysis tools for financial market data. It combines a Flask backend for data processing and API endpoints with a React frontend for user interaction.

## Project Structure
```
quant_analysis_project/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── user.py
│   │   └── stock.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── stock.py
│   │   └── admin.py
│   └── services/
│       ├── stock_service.py
│       ├── analysis_service.py
│       └── update_market_index.py
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── README.md
├── venv/
├── config.py
├── requirements.txt
├── run.py
└── manage_schedule.py
```

## Backend Setup

1. Create a virtual environment:
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS and Linux: `source venv/bin/activate`

3. Install required packages:
   ```
   pip install flask flask-sqlalchemy flask-migrate flask-login python-dotenv requests yfinance flask-cors flask-apscheduler
   ```

4. Create a `.env` file in the project root with the following content:
   ```
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=your_secret_key_here
   DATABASE_URL=mysql://username:password@localhost/quant_analysis_db
   ```

5. Initialize the database:
   ```
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

## Scheduled Tasks Setup

1. Market Data Updates:
   - The system automatically updates market indices every minute
   - Tracked indices include S&P 500, Dow 30, Nasdaq, Russell 2000, Crude Oil, and Gold

2. Running the Scheduler:
   ```bash
   # Ensure you're in virtual environment
   venv\Scripts\activate
   
   # Start the scheduler
   python manage_schedule.py
   ```

3. Scheduler Features:
   - Automatic market data updates every minute
   - Console logging of update status
   - Error handling and reporting

## Frontend Setup

[Previous frontend setup content remains the same...]

## Running the Application

1. Backend:
   - Activate the virtual environment
   - Run `flask run`

2. Frontend:
   - In a new terminal, navigate to the `frontend` directory
   - Run `npm start`

3. Scheduler:
   - In a separate terminal with activated virtual environment
   - Run `python manage_schedule.py`

The backend will be available at `http://localhost:5000`, and the frontend at `http://localhost:3000`.

## Current Features

- User registration and authentication
- Basic stock information retrieval
- Historical stock data fetching
- Fundamental metrics calculation
- Automated market index updates
- Real-time data monitoring

## API Endpoints

[Previous API endpoints content remains the same...]

## Test Account
```json
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpassword"
}
```

## Next Steps

- Implement frontend components for user registration and login
- Create stock search and display components
- Integrate frontend with backend API
- Implement more advanced analysis features
- Add data visualization for stock metrics and historical data
- Enhance scheduling capabilities and monitoring

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.