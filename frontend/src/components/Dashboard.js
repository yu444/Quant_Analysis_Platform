import React, { useState, useEffect } from 'react';

export default function Dashboard() {
  const [userData, setUserData] = useState(null);
  const [marketData, setMarketData] = useState(null);
  const [watchlist, setWatchlist] = useState([]);
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:5000/user', {
      credentials: 'include'
    })
      .then(response => response.ok ? response.json() : Promise.reject(response))
      .then(data => setUserData(data))
      .catch(error => console.error('Error fetching user data:', error));

    const fetchMarketData = () => {
      fetch('http://localhost:5000/market-indices/latest')
        .then(response => response.ok ? response.json() : Promise.reject(response))
        .then(data => {
          setMarketData(data.indices);
          setLoading(false);
        })
        .catch(error => {
          console.error('Error fetching market indices:', error);
          setLoading(false);
        });
    };

    fetchMarketData();
    const interval = setInterval(fetchMarketData, 300000);
    return () => clearInterval(interval);
  }, []);

  const formatNumber = (number) => {
    if (!number) return 'N/A';
    return new Intl.NumberFormat('en-US', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(number);
  };

  const renderHexagonCard = (indexData) => {
    if (!indexData) return null;
    const isPositive = indexData.daily_change > 0;
    const colorClass = isPositive ? 'bg-green-500' : 'bg-red-500';
    
    return (
      <div className="relative p-6 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow">
        {/* Hexagon indicator */}
        <div className="absolute -top-3 -right-3 w-12 h-12 flex items-center justify-center">
          <div className={`${colorClass} w-8 h-8 rotate-45 flex items-center justify-center`}>
            <span className="text-white -rotate-45 text-xl">
              {isPositive ? '▲' : '▼'}
            </span>
          </div>
        </div>
        
        {/* Content */}
        <div className="mb-4">
          <h3 className="text-lg font-bold text-gray-800">{indexData.name}</h3>
          <p className="text-3xl font-bold text-gray-900 mt-2">
            {formatNumber(indexData.latest_value)}
          </p>
        </div>
        
        {/* Metrics Grid */}
        <div className="grid grid-cols-2 gap-4 mt-4">
          <div className="bg-gray-50 p-2 rounded">
            <p className="text-sm text-gray-500">Change</p>
            <p className={`text-sm font-bold ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
              {isPositive ? '+' : ''}{formatNumber(indexData.daily_change)}
            </p>
          </div>
          <div className="bg-gray-50 p-2 rounded">
            <p className="text-sm text-gray-500">% Change</p>
            <p className={`text-sm font-bold ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
              {isPositive ? '+' : ''}{formatNumber(indexData.change_percent)}%
            </p>
          </div>
          <div className="bg-gray-50 p-2 rounded">
            <p className="text-sm text-gray-500">Volume</p>
            <p className="text-sm font-bold text-gray-800">
              {(indexData.volume / 1000000).toFixed(1)}M
            </p>
          </div>
          <div className="bg-gray-50 p-2 rounded">
            <p className="text-sm text-gray-500">Range</p>
            <p className="text-sm font-bold text-gray-800">
              {formatNumber(indexData.low)} - {formatNumber(indexData.high)}
            </p>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <h1 className="text-2xl font-bold text-gray-900">Market Dashboard</h1>
            <div className="text-sm text-gray-500">
              Last updated: {new Date().toLocaleTimeString()}
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Market Overview */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold text-gray-800">Market Overview</h2>
            <div className="flex items-center space-x-2">
              <div className={`w-3 h-3 rounded-full ${loading ? 'bg-yellow-400' : 'bg-green-400'}`}></div>
              <span className="text-sm text-gray-500">{loading ? 'Updating...' : 'Live'}</span>
            </div>
          </div>

          {loading ? (
            <div className="flex justify-center items-center h-64">
              <div className="animate-spin rounded-full h-12 w-12 border-4 border-blue-500 border-t-transparent"></div>
            </div>
          ) : marketData ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {Object.values(marketData).map((index) => (
                <div key={index.name}>{renderHexagonCard(index)}</div>
              ))}
            </div>
          ) : (
            <div className="text-center py-12 bg-white rounded-lg">
              <p className="text-gray-500">No market data available</p>
            </div>
          )}
        </div>

        {/* Lower Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Watchlist */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-bold text-gray-800">Watchlist</h2>
              <button className="text-blue-500 text-sm hover:text-blue-600">Edit</button>
            </div>
            {watchlist.length > 0 ? (
              <div className="space-y-3">
                {watchlist.map(stock => (
                  <div key={stock.symbol} className="flex justify-between items-center p-2 hover:bg-gray-50 rounded">
                    <div>
                      <p className="font-bold text-gray-800">{stock.symbol}</p>
                      <p className="text-sm text-gray-500">{stock.price}</p>
                    </div>
                    <div className="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center">
                      <span className="text-gray-600">→</span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8 text-gray-500">
                <p>No stocks in watchlist</p>
                <button className="mt-2 text-blue-500 hover:text-blue-600">Add stocks</button>
              </div>
            )}
          </div>

          {/* News Feed */}
          <div className="bg-white rounded-lg shadow-md p-6 lg:col-span-2">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-bold text-gray-800">Market News</h2>
              <button className="text-blue-500 text-sm hover:text-blue-600">View all</button>
            </div>
            {news.length > 0 ? (
              <div className="divide-y divide-gray-100">
                {news.map(item => (
                  <div key={item.id} className="py-4 hover:bg-gray-50">
                    <h3 className="font-medium text-gray-900">{item.headline}</h3>
                    <p className="text-sm text-gray-500 mt-1">
                      {new Date().toLocaleDateString()}
                    </p>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-12 text-gray-500">
                <p>No news available</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}