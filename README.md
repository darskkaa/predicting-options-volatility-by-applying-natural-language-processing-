# VOLA Engine

A simple stock analysis tool I built to track volatility and earnings. Made by Adil.

## What it does

- Shows stock prices and volatility
- Finds earnings dates
- Calculates basic financial metrics
- Works with real stock data

## How to use

1. Enter a stock symbol (like AAPL, TSLA, MSFT)
2. Get instant analysis with price data and volatility info
3. See earnings dates and basic metrics

## Local Development

### Backend
```bash
cd api
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Frontend  
```bash
cd app
npm run dev
```

## Deploy to Vercel

1. Push to GitHub
2. Connect to Vercel
3. Set environment variables:
   - `POLYGON_API_KEY`
   - `FMP_API_KEY`
4. Deploy!

## Made by Adil

This is my personal project for analyzing stock volatility. No AI, no fancy stuff - just straightforward financial analysis. 