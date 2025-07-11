# VOLA Engine

Advanced volatility analysis platform for quantitative research and financial analytics.

## Features

- Real-time stock data integration (Polygon.io, FMP, yfinance)
- Comprehensive volatility metrics and analysis
- Earnings data and market sentiment indicators
- Professional-grade API with detailed error handling
- Modern React frontend with real-time updates

## Quick Start

### Backend Setup
```bash
cd api
pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Frontend Setup
```bash
cd app
npm install
npm run dev
```

## API Documentation

### Core Endpoints

#### `GET /analyze/{ticker}`
Comprehensive stock analysis with volatility metrics.

**Response:**
```json
{
  "success": true,
  "ticker": "AAPL",
  "current_price": 150.25,
  "price_change": 2.50,
  "price_change_percent": 1.67,
  "volatility_30d": 18.5,
  "volatility_rating": "Moderate",
  "market_cap": 2500000000000,
  "volume": 45000000,
  "next_earnings": "2024-01-25",
  "analysis_summary": "AAPL is currently trading at $150.25 with a moderate volatility of 18.5%..."
}
```

#### `GET /health`
API health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Error Handling

The API provides detailed error responses with specific error codes and messages:

```json
{
  "success": false,
  "ticker": "INVALID",
  "error": "Data unavailable: No real data found for INVALID",
  "current_price": 0,
  "volatility_rating": "Error"
}
```

## Environment Variables

Create a `.env` file in the `api` directory:

```env
POLYGON_API_KEY=your_polygon_api_key
FMP_API_KEY=your_fmp_api_key
```

## Deployment

The application is configured for Vercel deployment with automatic API routing and environment variable management.

## Contributing

This project follows professional development practices with comprehensive error handling, detailed documentation, and clean code architecture. 