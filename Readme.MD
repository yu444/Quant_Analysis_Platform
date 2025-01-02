
# Quant Analysis Platform

Author: Joey Zhang
Last Updated: 2025-Jan-02

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Development Guide](#development-guide)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Quant Analysis Platform is a web-based application designed to provide quantitative analysis tools for financial market data. It combines a Flask backend for data processing and API endpoints with a React frontend for user interaction.

## Features

Current Features:
- Real-time market indices tracking (S&P 500, Dow 30, Nasdaq, Russell 2000, etc.)
- Automated market data updates
- Interactive dashboard with live updates
- Historical market data storage
- CORS-enabled API endpoints
- Real-time data monitoring with polling

Coming Soon:
- User authentication system
- Watchlist functionality
- Market news feed
- Advanced data visualization
- Technical analysis tools

## Project Structure

```
quant_analysis_platform/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── user.py
│   │   └── stock.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── stock.py
│   │   ├── market.py
│   │   └── admin.py
│   └── services/
│       ├── stock_service.py
│       ├── analysis_service.py
│       └── update_market_index.py
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   └── Dashboard.js
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── README.md
├── migrations/
├── venv/
├── config.py
├── requirements.txt
├── run.py
└── manage_schedule.py
```

## Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- MySQL 8.0 or higher
- Git

## Installation

### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/quant_analysis_platform.git
   cd quant_analysis_platform
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install required packages:
   ```bash
   pip install flask flask-sqlalchemy flask-migrate flask-login python-dotenv requests yfinance flask-cors flask-apscheduler pymysql
   ```

### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

### Database Setup

1. Create MySQL database:
   ```sql
   CREATE DATABASE quant_analysis_db;
   ```

2. Initialize the database:
   ```bash
   # Delete existing migrations if any
   rd /s /q migrations
   
   flask db init
   flask db migrate -m "create market indices table"
   flask db upgrade
   ```

## Configuration

1. Create `.env` file in project root:
   ```
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=your_secret_key_here
   DATABASE_URL=mysql://username:password@localhost/quant_analysis_db
   ```

2. Update database credentials in `.env` file with your MySQL credentials

## Running the Application

1. Start Backend Server (Terminal 1):
   ```bash
   # Activate virtual environment
   venv\Scripts\activate
   
   # Run Flask
   flask run
   ```
   Backend will be available at `http://localhost:5000`

2. Start Frontend Development Server (Terminal 2):
   ```bash
   cd frontend
   npm start
   ```
   Frontend will be available at `http://localhost:3000`

3. Start Market Data Scheduler (Terminal 3):
   ```bash
   # Activate virtual environment
   venv\Scripts\activate
   
   # Run scheduler
   python manage_schedule.py
   ```

## Development Guide

### Backend Development

1. Database Models (`app/models/`):
   - `stock.py`: Contains MarketIndex and other stock-related models
   - `user.py`: User model for authentication (coming soon)

2. Routes (`app/routes/`):
   - `market.py`: Market data endpoints
   - `auth.py`: Authentication endpoints (coming soon)
   - `admin.py`: Admin functionality (coming soon)

3. Services (`app/services/`):
   - `update_market_index.py`: Market data update service
   - `stock_service.py`: Stock data processing
   - `analysis_service.py`: Financial analysis calculations

### Frontend Development

1. Components:
   - `Dashboard.js`: Main dashboard component with market overview
   - More components coming soon

2. Features:
   - Real-time data updates using polling
   - Responsive design using Tailwind CSS
   - Interactive charts and visualizations

## API Documentation

### Market Data Endpoints

1. Get Latest Market Indices
   ```
   GET /market-indices/latest
   ```
   Returns the latest market data for all tracked indices

   Response Format:
   ```json
   {
     "date": "2025-01-02",
     "indices": {
       "S&P 500": {
         "name": "S&P 500",
         "latest_value": 4725.80,
         "daily_change": 25.30,
         "change_percent": 0.54,
         ...
       },
       ...
     }
   }
   ```

More endpoints coming soon.

## Troubleshooting

Common Issues:

1. Node.js not found:
   - Install Node.js from https://nodejs.org/
   - Ensure Node.js is added to system PATH

2. Database connection issues:
   - Verify MySQL is running
   - Check credentials in `.env` file
   - Ensure database exists

3. CORS issues:
   - Check CORS configuration in Flask app
   - Verify frontend URL in CORS settings

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

Please read CONTRIBUTING.md for detailed guidelines.

## License

This project is licensed under the MIT License - see LICENSE.md for details.
```

This README provides:
1. Clear installation instructions
2. Detailed project structure
3. Configuration requirements
4. Development guidelines
5. API documentation
6. Troubleshooting tips


######
######

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