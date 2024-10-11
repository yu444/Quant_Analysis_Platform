import React, { useState, useEffect } from 'react';
import axios from 'axios';
import styled from 'styled-components';

const DashboardContainer = styled.div`
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  padding: 20px;
  background-color: #f0f2f5;
`;

const Widget = styled.div`
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

const Title = styled.h2`
  color: #333;
  font-size: 18px;
  margin-bottom: 15px;
`;

const UserWelcome = styled(Widget)`
  grid-column: span 3;
`;

const MarketOverview = styled(Widget)`
  grid-column: span 2;
`;

const Watchlist = styled(Widget)`
  grid-column: span 1;
`;

const NewsFeed = styled(Widget)`
  grid-column: span 2;
`;

const QuickActions = styled(Widget)`
  grid-column: span 1;
`;

function Dashboard() {
  const [userData, setUserData] = useState(null);
  const [marketData, setMarketData] = useState(null);
  const [watchlist, setWatchlist] = useState([]);
  const [news, setNews] = useState([]);

  useEffect(() => {
    // Fetch user data
    axios.get('http://localhost:5000/user', { 
        withCredentials: true  // This is crucial for sending cookies
      })
        .then(response => setUserData(response.data))
        .catch(error => {
          console.error('Error fetching user data:', error);
          // Handle unauthorized access, e.g., redirect to login page
          if (error.response && error.response.status === 401) {
            // Redirect to login page or show login prompt
          }
        });

    // Fetch market data (you'll need to implement this endpoint)
   /* axios.get('http://localhost:5000/market-overview')
      .then(response => setMarketData(response.data))
      .catch(error => console.error('Error fetching market data:', error));

    // Fetch watchlist (you'll need to implement this endpoint)
    axios.get('http://localhost:5000/watchlist')
      .then(response => setWatchlist(response.data))
      .catch(error => console.error('Error fetching watchlist:', error));

    // Fetch news (you'll need to implement this endpoint)
    axios.get('http://localhost:5000/news')
      .then(response => setNews(response.data))
      .catch(error => console.error('Error fetching news:', error));*/
  }, []);

  if (!userData) return <div>Loading...</div>;

  return (
    <DashboardContainer>
      <UserWelcome>
        <Title>Welcome, {userData.username}!</Title>
        <p>Last login: {new Date().toLocaleString()}</p>
      </UserWelcome>

      <MarketOverview>
        <Title>Market Overview</Title>
        {marketData ? (
          <div>
            <p>S&P 500: {marketData.sp500}</p>
            <p>NASDAQ: {marketData.nasdaq}</p>
            <p>Dow Jones: {marketData.dowJones}</p>
          </div>
        ) : (
          <p>Loading market data...</p>
        )}
      </MarketOverview>

      <Watchlist>
        <Title>Your Watchlist</Title>
        {watchlist.length > 0 ? (
          <ul>
            {watchlist.map(stock => (
              <li key={stock.symbol}>{stock.symbol}: ${stock.price}</li>
            ))}
          </ul>
        ) : (
          <p>No stocks in watchlist</p>
        )}
      </Watchlist>

      <NewsFeed>
        <Title>Latest News</Title>
        {news.length > 0 ? (
          <ul>
            {news.slice(0, 5).map(item => (
              <li key={item.id}>{item.headline}</li>
            ))}
          </ul>
        ) : (
          <p>No news available</p>
        )}
      </NewsFeed>

      <QuickActions>
        <Title>Quick Actions</Title>
        <button>Analyze Stock</button>
        <button>View Portfolio</button>
        <button>Set Alert</button>
      </QuickActions>
    </DashboardContainer>
  );
}

export default Dashboard;