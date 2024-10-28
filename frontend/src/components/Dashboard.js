import React, { useState, useEffect } from 'react';

export default function Dashboard() {
  const [userData, setUserData] = useState(null);
  const [marketData, setMarketData] = useState({});
  const [watchlist, setWatchlist] = useState([]);
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch user data
    const fetchUserData = async () => {
      try {
        const response = await fetch('http://localhost:5000/user', {
          credentials: 'include'
        });
        if (response.ok) {
          const data = await response.json();
          setUserData(data);
        }
      } catch (error) {
        console.error('Error fetching user data:', error);
        setUserData({ username: 'Guest' });
      }
    };

    // Fetch market indices data
    const fetchMarketData = async () => {
      setLoading(true);
      try {
        const response = await fetch('http://localhost:5000/market-indices/latest', {
          //credentials: 'include'
        });
        if (!response.ok) {
          throw new Error('Failed to fetch market data');
        }
        const data = await response.json();
        console.log('Market data received:', data);
        setMarketData(data.indices || {});
        setError(null);
      } catch (error) {
        console.error('Error fetching market data:', error);
        setError('Failed to load market data');
      } finally {
        setLoading(false);
      }
    };

    // Initial data fetch
    fetchUserData();
    fetchMarketData();

    // Set up polling for market data
    const intervalId = setInterval(fetchMarketData, 300000); // 5 minutes

    return () => clearInterval(intervalId);
  }, []);

  const formatNumber = (number) => {
    if (number === null || number === undefined) return 'N/A';
    return new Intl.NumberFormat('en-US', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(number);
  };

  const formatVolume = (volume) => {
    if (!volume) return 'N/A';
    if (volume >= 1000000000) {
      return `${(volume / 1000000000).toFixed(1)}B`;
    }
    return `${(volume / 1000000).toFixed(1)}M`;
  };

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-xl font-semibold text-gray-900">Error Loading Data</h2>
          <p className="text-gray-500 mt-2">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation Bar */}
      <nav className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-gray-900">Quant Analysis Platform</h1>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-sm text-gray-500">
                {userData?.username && `Welcome, ${userData.username}`}
              </div>
              <button className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                My Account
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Market Overview Section */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-2xl font-bold text-gray-900">Market Overview</h2>
              <p className="text-sm text-gray-500 mt-1">Real-time market indices and performance</p>
            </div>
            <div className="flex items-center space-x-3">
              <div className={`h-2 w-2 rounded-full ${loading ? 'bg-yellow-400' : 'bg-emerald-400'}`} />
              <span className="text-sm text-gray-600">{loading ? 'Updating...' : 'Live'}</span>
              <span className="text-sm text-gray-400">
                Last updated: {new Date().toLocaleTimeString()}
              </span>
            </div>
          </div>

          {loading && Object.keys(marketData).length === 0 ? (
            <div className="flex justify-center items-center h-64">
              <div className="animate-spin rounded-full h-12 w-12 border-4 border-indigo-500 border-t-transparent"></div>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {Object.values(marketData).map((index) => (
                <div key={index.name} className="bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow duration-200 overflow-hidden">
                  <div className={`h-1 ${index.daily_change > 0 ? 'bg-emerald-500' : 'bg-red-500'}`} />
                  <div className="p-6">
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900">{index.name}</h3>
                        <p className="text-3xl font-bold tracking-tight text-gray-900 mt-2">
                          {formatNumber(index.latest_value)}
                        </p>
                      </div>
                      <div className={`px-3 py-1 rounded-full ${
                        index.daily_change > 0 ? 'bg-emerald-50 text-emerald-700' : 'bg-red-50 text-red-700'
                      }`}>
                        {index.daily_change > 0 ? '▲' : '▼'} {Math.abs(index.change_percent).toFixed(2)}%
                      </div>
                    </div>

                    <div className="grid grid-cols-2 gap-3">
                      <div className="bg-gray-50 rounded-lg p-3">
                        <div className="text-sm font-medium text-gray-500">Daily Change</div>
                        <div className={`text-sm font-semibold ${
                          index.daily_change > 0 ? 'text-emerald-600' : 'text-red-600'
                        }`}>
                          {index.daily_change > 0 ? '+' : ''}
                          {formatNumber(index.daily_change)}
                        </div>
                      </div>
                      <div className="bg-gray-50 rounded-lg p-3">
                        <div className="text-sm font-medium text-gray-500">Volume</div>
                        <div className="text-sm font-semibold text-gray-900">
                          {formatVolume(index.volume)}
                        </div>
                      </div>
                      <div className="bg-gray-50 rounded-lg p-3 col-span-2">
                        <div className="text-sm font-medium text-gray-500">Today's Range</div>
                        <div className="mt-1 relative h-1.5 bg-gray-200 rounded-full">
                          <div className="absolute inset-y-0 bg-indigo-600 rounded-full" 
                               style={{
                                 left: `${((index.latest_value - index.low) / (index.high - index.low)) * 100}%`,
                                 width: '4px'
                               }} />
                        </div>
                        <div className="flex justify-between mt-1">
                          <span className="text-xs font-medium text-gray-500">
                            {formatNumber(index.low)}
                          </span>
                          <span className="text-xs font-medium text-gray-500">
                            {formatNumber(index.high)}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Lower Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Watchlist Panel */}
          <div className="bg-white rounded-xl shadow-sm">
            <div className="p-6">
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h2 className="text-lg font-semibold text-gray-900">Watchlist</h2>
                  <p className="text-sm text-gray-500 mt-1">Coming Soon</p>
                </div>
                <button className="inline-flex items-center px-3 py-1.5 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50">
                  Add Stock
                </button>
              </div>
              
              <div className="text-center py-8 text-gray-500">
                <p>Watchlist feature will be available soon</p>
              </div>
            </div>
          </div>

          {/* News Panel */}
          <div className="bg-white rounded-xl shadow-sm lg:col-span-2">
            <div className="p-6">
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h2 className="text-lg font-semibold text-gray-900">Market News</h2>
                  <p className="text-sm text-gray-500 mt-1">Coming Soon</p>
                </div>
                <button className="text-indigo-600 hover:text-indigo-700 text-sm font-medium">
                  View All
                </button>
              </div>
              
              <div className="text-center py-8 text-gray-500">
                <p>News feed will be available soon</p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}