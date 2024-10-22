import React, { useState, useEffect } from 'react';
import { TrendingUp, TrendingDown, Activity } from 'lucide-react';

export default function Dashboard() {
  const [userData, setUserData] = useState(null);
  const [marketData, setMarketData] = useState(null);
  const [watchlist, setWatchlist] = useState([]);
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch user data
    fetch('http://localhost:5000/user', {
      credentials: 'include'  // Equivalent to axios withCredentials
    })
      .then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
      })
      .then(data => setUserData(data))
      .catch(error => {
        console.error('Error fetching user data:', error);
        if (error.response?.status === 401) {
          // Handle unauthorized access
        }
      });

    // Fetch market indices data using the new endpoint
    const fetchMarketData = () => {
      fetch('http://localhost:5000/market-indices/latest')
        .then(response => {
          if (!response.ok) throw new Error('Network response was not ok');
          return response.json();
        })
        .then(data => {
          console.log('Market Indices Data:', data);
          setMarketData(data.indices);
          setLoading(false);
        })
        .catch(error => {
          console.error('Error fetching market indices:', error);
          setLoading(false);
        });
    };

    fetchMarketData();
    // Update market data every 5 minutes
    const interval = setInterval(fetchMarketData, 300000);

    return () => clearInterval(interval);
  }, []);

  const formatNumber = (number) => {
    return new Intl.NumberFormat('en-US', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(number);
  };

  const renderMarketIndex = (indexData) => {
    if (!indexData) return null;

    const isPositive = indexData.daily_change > 0;
    const Icon = isPositive ? TrendingUp : TrendingDown;
    const colorClass = isPositive ? 'text-green-600' : 'text-red-600';

    return (
      <div className="p-4 bg-white rounded-lg shadow-sm">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-lg font-semibold text-gray-800">{indexData.name}</h3>
          <Icon className={`w-5 h-5 ${colorClass}`} />
        </div>
        <div className="text-2xl font-bold mb-2">
          {formatNumber(indexData.latest_value)}
        </div>
        <div className={`flex items-center ${colorClass}`}>
          <span className="font-medium">
            {isPositive ? '+' : ''}{formatNumber(indexData.daily_change)} 
          </span>
          <span className="ml-2">
            ({formatNumber(indexData.change_percent)}%)
          </span>
        </div>
        <div className="mt-2 text-sm text-gray-500">
          Volume: {indexData.volume?.toLocaleString()}
        </div>
        <div className="mt-1 text-sm text-gray-500">
          Range: {formatNumber(indexData.low)} - {formatNumber(indexData.high)}
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      {/* Welcome Section */}
      <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
        <h1 className="text-2xl font-bold text-gray-800">
          Welcome, {userData?.username || 'User'}!
        </h1>
        <p className="text-gray-600">
          Last login: {new Date().toLocaleString()}
        </p>
      </div>

      {/* Market Overview Section */}
      <div className="mb-6">
        <div className="flex items-center mb-4">
          <Activity className="w-6 h-6 text-blue-600 mr-2" />
          <h2 className="text-xl font-bold text-gray-800">Market Overview</h2>
        </div>
        
        {loading ? (
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading market data...</p>
          </div>
        ) : marketData ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {Object.values(marketData).map((index) => (
              <div key={index.name}>
                {renderMarketIndex(index)}
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8 text-gray-600">
            No market data available
          </div>
        )}
      </div>

      {/* Additional Sections */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Watchlist */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4">Your Watchlist</h2>
          {watchlist.length > 0 ? (
            <ul className="space-y-2">
              {watchlist.map(stock => (
                <li key={stock.symbol} className="flex justify-between items-center">
                  <span className="font-medium">{stock.symbol}</span>
                  <span>${stock.price}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-gray-600">No stocks in watchlist</p>
          )}
        </div>

        {/* News Feed */}
        <div className="bg-white rounded-lg shadow-sm p-6 md:col-span-2">
          <h2 className="text-xl font-bold text-gray-800 mb-4">Latest News</h2>
          {news.length > 0 ? (
            <ul className="space-y-3">
              {news.slice(0, 5).map(item => (
                <li key={item.id} className="border-b border-gray-100 pb-2">
                  {item.headline}
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-gray-600">No news available</p>
          )}
        </div>
      </div>

      {/* Quick Actions */}
      <div className="fixed bottom-6 right-6">
        <div className="flex space-x-2">
          <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
            Analyze Stock
          </button>
          <button className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors">
            View Portfolio
          </button>
          <button className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors">
            Set Alert
          </button>
        </div>
      </div>
    </div>
  );
}