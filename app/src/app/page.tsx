'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';

interface StockData {
  success: boolean;
  ticker: string;
  current_price: number;
  price_change: number;
  price_change_percent: number;
  market_cap: number;
  volume: number;
  avg_volume: number;
  high: number;
  low: number;
  open: number;
  volatility_30d: number;
  volatility_rating: string;
  next_earnings: string;
  earnings_date: string;
  data_source: string;
  timestamp: string;
  error?: string;
}

interface SentimentData {
  overall_sentiment: string;
  sentiment_score: number;
  key_phrases: string[];
  risk_indicators: string[];
}

const formatLargeNumber = (num: number): string => {
  if (num >= 1e12) return (num / 1e12).toFixed(1) + 'T';
  if (num >= 1e9) return (num / 1e9).toFixed(1) + 'B';
  if (num >= 1e6) return (num / 1e6).toFixed(1) + 'M';
  if (num >= 1e3) return (num / 1e3).toFixed(1) + 'K';
  return num.toString();
};

export default function Home() {
  const [stockData, setStockData] = useState<StockData | null>(null);
  const [sentimentData, setSentimentData] = useState<SentimentData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [symbol, setSymbol] = useState('AAPL');
  const [searchInput, setSearchInput] = useState('AAPL');

  const fetchStockData = async (stockSymbol: string) => {
    if (!stockSymbol.trim()) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`/api/analyze/${stockSymbol.toUpperCase()}`);
      if (!response.ok) {
        throw new Error(`Failed to fetch data: ${response.status}`);
      }
      const data = await response.json();
      
      if (data.success === false) {
        setError(data.error || 'Failed to fetch stock data');
        setStockData(null);
      } else {
        setStockData(data);
        setError(null);
      }
      
      // Fetch sentiment analysis (if endpoint exists)
      try {
        const sentimentResponse = await fetch(`/api/sentiment/${stockSymbol.toUpperCase()}`);
        if (sentimentResponse.ok) {
          const sentimentData = await sentimentResponse.json();
          setSentimentData(sentimentData);
        }
      } catch (sentimentError) {
        console.log('Sentiment analysis not available');
      }
    } catch (error) {
      console.error('Error fetching stock data:', error);
      setError(error instanceof Error ? error.message : 'Failed to fetch data');
      setStockData(null);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = () => {
    if (searchInput.trim()) {
      setSymbol(searchInput.toUpperCase());
      fetchStockData(searchInput.toUpperCase());
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  useEffect(() => {
    fetchStockData(symbol);
  }, []);

  const chartData = stockData ? [
    { period: 'Current', volatility: stockData.volatility_30d },
    { period: '3 Month', volatility: stockData.volatility_30d * 0.9 },
    { period: '6 Month', volatility: stockData.volatility_30d * 1.1 }
  ] : [];

  const getVolatilityColor = (volatility: number) => {
    if (volatility > 30) return 'text-red-400';
    if (volatility > 20) return 'text-yellow-400';
    return 'text-green-400';
  };

  const getSentimentColor = (sentiment: string) => {
    if (sentiment.includes('positive')) return 'text-green-400';
    if (sentiment.includes('negative')) return 'text-red-400';
    return 'text-yellow-400';
  };

  const getPriceChangeColor = (change: number) => {
    if (change > 0) return 'text-green-400';
    if (change < 0) return 'text-red-400';
    return 'text-gray-400';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white">
      <div className="container mx-auto px-6 py-10 max-w-7xl">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-16"
        >
          <h1 className="text-8xl font-bold mb-8 bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
            VOLA Engine
          </h1>
          <p className="text-4xl text-gray-300 mb-4">Volatility Linguistics Arbitrage</p>
          <p className="text-2xl text-gray-400">Advanced NLP-powered stock volatility analysis</p>
        </motion.div>

        {/* Search Bar */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-16"
        >
          <div className="flex justify-center">
            <div className="relative w-full max-w-3xl">
              <input
                type="text"
                value={searchInput}
                onChange={(e) => setSearchInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Enter stock symbol (e.g., AAPL, TSLA, META)..."
                className="w-full px-10 py-8 bg-white/10 backdrop-blur-sm border border-white/20 rounded-2xl text-white placeholder-gray-400 focus:outline-none focus:ring-4 focus:ring-purple-500/50 text-3xl font-medium"
              />
              <button
                onClick={handleSearch}
                disabled={loading}
                className="absolute right-6 top-1/2 transform -translate-y-1/2 px-10 py-4 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 rounded-xl text-2xl font-semibold transition-all duration-200 shadow-lg hover:shadow-xl disabled:opacity-50"
              >
                {loading ? (
                  <div className="flex items-center">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-white mr-4"></div>
                    <span className="text-2xl">Analyzing...</span>
                  </div>
                ) : (
                  'Analyze'
                )}
              </button>
            </div>
          </div>
        </motion.div>

        {/* Error Display */}
        {error && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-8 p-6 bg-red-500/20 border border-red-500/30 rounded-xl text-red-300 text-xl"
          >
            <p className="text-center">{error}</p>
          </motion.div>
        )}

        {/* Stock Data Display */}
        {stockData && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-12"
          >
            {/* Stock Header */}
            <div className="glassmorphism p-12">
              <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-8">
                <div>
                  <h2 className="text-8xl font-bold mb-4">{stockData.ticker}</h2>
                  <p className="text-4xl text-gray-300 mb-4">Stock Analysis</p>
                  <p className="text-2xl text-gray-400">Data Source: {stockData.data_source}</p>
                </div>
                <div className="text-right">
                  <p className="text-8xl font-bold">${stockData.current_price?.toFixed(2) || 'N/A'}</p>
                  <div className="flex items-center justify-end mt-4">
                    <span className={`text-3xl font-bold ${getPriceChangeColor(stockData.price_change)}`}>
                      {stockData.price_change > 0 ? '+' : ''}{stockData.price_change?.toFixed(2) || '0.00'}
                    </span>
                    <span className={`text-2xl ml-2 ${getPriceChangeColor(stockData.price_change_percent)}`}>
                      ({stockData.price_change_percent > 0 ? '+' : ''}{stockData.price_change_percent?.toFixed(2) || '0.00'}%)
                    </span>
                  </div>
                  <p className="text-3xl text-gray-400 mt-4">Current Price</p>
                </div>
              </div>
            </div>

            {/* Key Metrics Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
              <motion.div
                whileHover={{ scale: 1.02 }}
                className="glassmorphism p-8 card-hover"
              >
                <div className="text-center">
                  <p className={`text-6xl font-bold ${getVolatilityColor(stockData.volatility_30d)}`}>
                    {stockData.volatility_30d?.toFixed(1) || 'N/A'}%
                  </p>
                  <p className="text-2xl text-gray-400 mt-4">30-day Volatility</p>
                  <p className="text-xl text-gray-500 mt-2">{stockData.volatility_rating}</p>
                </div>
              </motion.div>

              <motion.div
                whileHover={{ scale: 1.02 }}
                className="glassmorphism p-8 card-hover"
              >
                <div className="text-center">
                  <p className="text-5xl font-bold">{stockData.next_earnings || 'N/A'}</p>
                  <p className="text-2xl text-gray-400 mt-4">Next Earnings</p>
                  <p className="text-xl text-gray-500 mt-2">{stockData.earnings_date}</p>
                </div>
              </motion.div>

              <motion.div
                whileHover={{ scale: 1.02 }}
                className="glassmorphism p-8 card-hover"
              >
                <div className="text-center">
                  <p className="text-5xl font-bold">{formatLargeNumber(stockData.market_cap || 0)}</p>
                  <p className="text-2xl text-gray-400 mt-4">Market Cap</p>
                </div>
              </motion.div>

              <motion.div
                whileHover={{ scale: 1.02 }}
                className="glassmorphism p-8 card-hover"
              >
                <div className="text-center">
                  <p className="text-5xl font-bold">{formatLargeNumber(stockData.avg_volume || 0)}</p>
                  <p className="text-2xl text-gray-400 mt-4">Avg Volume</p>
                </div>
              </motion.div>
            </div>

            {/* Additional Stock Data */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <motion.div
                whileHover={{ scale: 1.02 }}
                className="glassmorphism p-8 card-hover"
              >
                <div className="text-center">
                  <p className="text-4xl font-bold">${stockData.high?.toFixed(2) || 'N/A'}</p>
                  <p className="text-xl text-gray-400 mt-2">Day High</p>
                </div>
              </motion.div>

              <motion.div
                whileHover={{ scale: 1.02 }}
                className="glassmorphism p-8 card-hover"
              >
                <div className="text-center">
                  <p className="text-4xl font-bold">${stockData.low?.toFixed(2) || 'N/A'}</p>
                  <p className="text-xl text-gray-400 mt-2">Day Low</p>
                </div>
              </motion.div>

              <motion.div
                whileHover={{ scale: 1.02 }}
                className="glassmorphism p-8 card-hover"
              >
                <div className="text-center">
                  <p className="text-4xl font-bold">{formatLargeNumber(stockData.volume || 0)}</p>
                  <p className="text-xl text-gray-400 mt-2">Volume</p>
                </div>
              </motion.div>
            </div>

            {/* Analysis Summary */}
            <div className="glassmorphism p-12">
              <h3 className="text-4xl font-semibold mb-6">Analysis Summary</h3>
              <p className="text-2xl text-gray-300 leading-relaxed">
                {stockData.ticker} is currently trading at ${stockData.current_price?.toFixed(2) || 'N/A'} with a 
                {stockData.volatility_30d > 25 ? ' high' : stockData.volatility_30d > 15 ? ' moderate' : ' low'} 
                volatility of {stockData.volatility_30d?.toFixed(1) || 'N/A'}%. The stock has a market cap of 
                {formatLargeNumber(stockData.market_cap || 0)} and average volume of {formatLargeNumber(stockData.avg_volume || 0)} shares.
                {stockData.next_earnings && stockData.next_earnings !== 'N/A' ? 
                  ` Next earnings are expected ${stockData.next_earnings}.` : ''}
              </p>
            </div>

            {/* Volatility Chart */}
            <div className="glassmorphism p-12">
              <h3 className="text-4xl font-semibold mb-8">Volatility Comparison</h3>
              <div className="h-96">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                    <XAxis dataKey="period" stroke="#9CA3AF" fontSize={18} />
                    <YAxis stroke="#9CA3AF" fontSize={18} />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: '#1F2937',
                        border: '1px solid #374151',
                        borderRadius: '8px',
                        color: '#F9FAFB',
                        fontSize: '16px'
                      }}
                    />
                    <Bar dataKey="volatility" fill="#8B5CF6" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Sentiment Analysis */}
            {sentimentData && (
              <div className="glassmorphism p-12">
                <h3 className="text-4xl font-semibold mb-8">Sentiment Analysis</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                  <div>
                    <h4 className="text-2xl font-semibold mb-4">Overall Sentiment</h4>
                    <p className={`text-4xl font-bold ${getSentimentColor(sentimentData.overall_sentiment)}`}>
                      {sentimentData.overall_sentiment}
                    </p>
                    <p className="text-xl text-gray-400 mt-2">Score: {sentimentData.sentiment_score?.toFixed(2)}</p>
                  </div>
                  <div>
                    <h4 className="text-2xl font-semibold mb-4">Key Phrases</h4>
                    <div className="flex flex-wrap gap-3">
                      {sentimentData.key_phrases?.map((phrase, index) => (
                        <span key={index} className="px-4 py-2 bg-purple-600/20 border border-purple-500/30 rounded-full text-lg">
                          {phrase}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
                {sentimentData.risk_indicators && sentimentData.risk_indicators.length > 0 && (
                  <div className="mt-8">
                    <h4 className="text-2xl font-semibold mb-4">Risk Indicators</h4>
                    <div className="space-y-3">
                      {sentimentData.risk_indicators.map((indicator, index) => (
                        <p key={index} className="text-red-400 text-lg">Warning: {indicator}</p>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </motion.div>
        )}

        {/* Loading State */}
        {loading && !stockData && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center py-24"
          >
            <div className="animate-spin rounded-full h-20 w-20 border-b-2 border-purple-500 mx-auto mb-6"></div>
            <p className="text-3xl text-gray-300">Analyzing stock data...</p>
          </motion.div>
        )}
      </div>

      <style jsx>{`
        .glassmorphism {
          background: rgba(255, 255, 255, 0.05);
          backdrop-filter: blur(10px);
          border: 1px solid rgba(255, 255, 255, 0.1);
          border-radius: 20px;
        }
        
        .card-hover {
          transition: all 0.3s ease;
        }
        
        .card-hover:hover {
          background: rgba(255, 255, 255, 0.08);
          border-color: rgba(139, 92, 246, 0.3);
          transform: translateY(-4px);
        }
      `}</style>
    </div>
  );
}
