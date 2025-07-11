"""
VOLA Engine API

This FastAPI application provides endpoints for real-time stock volatility analysis, integrating with Polygon.io, FMP, and yfinance APIs. Optimized for Netlify Functions deployment.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import requests
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
from typing import Dict, Any, Optional
from pydantic import BaseModel
import time
import random

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="VOLA Engine API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for Netlify
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Keys
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
FMP_API_KEY = os.getenv("FMP_API_KEY")

class StockRequest(BaseModel):
    ticker: str

@app.get("/")
def read_root():
    return {"message": "VOLA Engine API is running!", "status": "success"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

def generate_analysis_summary(ticker: str, stock_data: dict, volatility_data: dict, earnings_data: dict) -> str:
    price = stock_data.get("price", 0)
    volatility = volatility_data.get("annualized_volatility", 0)
    market_cap = stock_data.get("market_cap", 0)
    avg_volume = stock_data.get("avg_volume", 0)
    next_earnings = earnings_data.get("next_earnings", "N/A")

    # Volatility description
    if volatility > 25:
        vol_desc = "high"
    elif volatility > 15:
        vol_desc = "moderate"
    else:
        vol_desc = "low"

    return (
        f"{ticker} is currently trading at ${price:.2f} with a {vol_desc} volatility of {volatility:.1f}%. "
        f"The stock has a market cap of {market_cap:,} and average volume of {avg_volume:,} shares."
        + (f" Next earnings are expected {next_earnings}." if next_earnings and next_earnings != 'N/A' else "")
    )

@app.get("/analyze/{ticker}")
async def analyze_stock(ticker: str):
    """Analyze any stock ticker with comprehensive data and improved error handling"""
    ticker = ticker.upper()
    
    try:
        # Get comprehensive stock data
        stock_data = get_comprehensive_stock_data(ticker)
        earnings_data = get_earnings_data(ticker)
        volatility_data = calculate_volatility(ticker)

        analysis_summary = generate_analysis_summary(
            ticker, stock_data, volatility_data, earnings_data
        )
        
        # Format the response for frontend
        formatted_response = {
            "success": True,
            "ticker": ticker,
            "current_price": stock_data.get("price", 0),
            "price_change": stock_data.get("price_change", 0),
            "price_change_percent": stock_data.get("price_change_percent", 0),
            "market_cap": stock_data.get("market_cap", 0),
            "volume": stock_data.get("volume", 0),
            "avg_volume": stock_data.get("avg_volume", 0),
            "high": stock_data.get("high", 0),
            "low": stock_data.get("low", 0),
            "open": stock_data.get("open", 0),
            "volatility_30d": volatility_data.get("annualized_volatility", 0),
            "volatility_rating": volatility_data.get("volatility_rating", "Unknown"),
            "next_earnings": earnings_data.get("next_earnings", "N/A"),
            "earnings_date": earnings_data.get("earnings_date", "N/A"),
            "data_source": stock_data.get("source", "Unknown"),
            "timestamp": datetime.now().isoformat(),
            "analysis_summary": analysis_summary,
            "raw_data": {
                "stock_data": stock_data,
                "earnings_data": earnings_data,
                "volatility_data": volatility_data
            }
        }
        
        return formatted_response
        
    except HTTPException as e:
        print(f"HTTP error analyzing {ticker}: {e.detail}")
        return {
            "success": False,
            "ticker": ticker,
            "error": f"Data unavailable: {e.detail}",
            "current_price": 0,
            "price_change": 0,
            "price_change_percent": 0,
            "market_cap": 0,
            "volume": 0,
            "avg_volume": 0,
            "high": 0,
            "low": 0,
            "open": 0,
            "volatility_30d": 0,
            "volatility_rating": "Error",
            "next_earnings": "N/A",
            "earnings_date": "N/A",
            "data_source": "Error",
            "timestamp": datetime.now().isoformat(),
            "analysis_summary": "No analysis available due to data error."
        }
    except Exception as e:
        print(f"Unexpected error analyzing {ticker}: {e}")
        return {
            "success": False,
            "ticker": ticker,
            "error": f"Analysis failed: {str(e)}",
            "current_price": 0,
            "price_change": 0,
            "price_change_percent": 0,
            "market_cap": 0,
            "volume": 0,
            "avg_volume": 0,
            "high": 0,
            "low": 0,
            "open": 0,
            "volatility_30d": 0,
            "volatility_rating": "Error",
            "next_earnings": "N/A",
            "earnings_date": "N/A",
            "data_source": "Error",
            "timestamp": datetime.now().isoformat(),
            "analysis_summary": "No analysis available due to unexpected error."
        }

def get_comprehensive_stock_data(ticker: str) -> dict:
    """Get comprehensive stock data with proper formatting and real API fallback only"""
    # Try yfinance first (most reliable for Netlify)
    yf_data = get_yfinance_data(ticker)
    if yf_data and yf_data.get("price", 0) > 0:
        return yf_data
    # Try Polygon.io
    polygon_data = get_polygon_data(ticker)
    if polygon_data and polygon_data.get("price", 0) > 0:
        return polygon_data
    # Try FMP
    fmp_data = get_fmp_data(ticker)
    if fmp_data and fmp_data.get("price", 0) > 0:
        return fmp_data
    # If all fail, raise error
    raise HTTPException(status_code=404, detail=f"No real data found for {ticker}")

def get_yfinance_data(ticker: str) -> Optional[Dict[str, Any]]:
    """Get data from yfinance with improved error handling"""
    try:
        # Add delay to avoid rate limiting
        time.sleep(random.uniform(0.5, 1.5))
        
        stock = yf.Ticker(ticker)
        
        # Get historical data first
        hist = stock.history(period="5d")
        
        if not hist.empty and len(hist) > 1:
            current_price = float(hist['Close'].iloc[-1])
            prev_price = float(hist['Close'].iloc[-2])
            price_change = current_price - prev_price
            price_change_percent = (price_change / prev_price) * 100 if prev_price > 0 else 0
            
            # Get additional info with error handling
            try:
                info = stock.info
                market_cap = int(info.get('marketCap', 0))
                avg_volume = int(info.get('averageVolume', 0))
            except:
                market_cap = 0
                avg_volume = 0
            
            return {
                "price": current_price,
                "price_change": price_change,
                "price_change_percent": price_change_percent,
                "market_cap": market_cap,
                "volume": int(hist['Volume'].iloc[-1]),
                "avg_volume": avg_volume,
                "high": float(hist['High'].iloc[-1]),
                "low": float(hist['Low'].iloc[-1]),
                "open": float(hist['Open'].iloc[-1]),
                "source": "Yahoo Finance"
            }
        return None
    except Exception as e:
        print(f"Error getting yfinance data for {ticker}: {e}")
        return None

def get_polygon_data(ticker: str) -> Optional[Dict[str, Any]]:
    """Get data from Polygon.io API"""
    if not POLYGON_API_KEY:
        return None
    
    try:
        # Get current price
        url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/prev?adjusted=true&apiKey={POLYGON_API_KEY}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('results') and len(data['results']) > 0:
                result = data['results'][0]
                current_price = float(result['c'])
                prev_price = float(result['o'])
                price_change = current_price - prev_price
                price_change_percent = (price_change / prev_price) * 100 if prev_price > 0 else 0
                
                return {
                    "price": current_price,
                    "price_change": price_change,
                    "price_change_percent": price_change_percent,
                    "market_cap": 0,  # Polygon doesn't provide this in basic endpoint
                    "volume": int(result['v']),
                    "avg_volume": 0,
                    "high": float(result['h']),
                    "low": float(result['l']),
                    "open": prev_price,
                    "source": "Polygon.io"
                }
        return None
    except Exception as e:
        print(f"Error getting Polygon data for {ticker}: {e}")
        return None

def get_fmp_data(ticker: str) -> Optional[dict]:
    """Get data from Financial Modeling Prep API"""
    if not FMP_API_KEY:
        return None
    
    try:
        # Get quote
        url = f"https://financialmodelingprep.com/api/v3/quote/{ticker}?apikey={FMP_API_KEY}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                quote = data[0]
                current_price = float(quote.get('price', 0))
                prev_price = float(quote.get('previousClose', current_price))
                price_change = current_price - prev_price
                price_change_percent = (price_change / prev_price) * 100 if prev_price > 0 else 0
                
                return {
                    "price": current_price,
                    "price_change": price_change,
                    "price_change_percent": price_change_percent,
                    "market_cap": int(quote.get('marketCap', 0)),
                    "volume": int(quote.get('volume', 0)),
                    "avg_volume": int(quote.get('avgVolume', 0)),
                    "high": float(quote.get('dayHigh', 0)),
                    "low": float(quote.get('dayLow', 0)),
                    "open": float(quote.get('open', 0)),
                    "source": "Financial Modeling Prep"
                }
        return None
    except Exception as e:
        print(f"Error getting FMP data for {ticker}: {e}")
        return None

def get_earnings_data(ticker: str) -> Dict[str, Any]:
    """Get earnings data for a stock"""
    try:
        stock = yf.Ticker(ticker)
        calendar = stock.calendar
        
        if calendar is not None and isinstance(calendar, pd.DataFrame) and not calendar.empty:
            next_earnings = calendar.iloc[0]['Earnings Date']
            if isinstance(next_earnings, pd.Timestamp):
                next_earnings = next_earnings.strftime('%Y-%m-%d')
            
            return {
                "next_earnings": next_earnings,
                "earnings_date": next_earnings
            }
        else:
            return {
                "next_earnings": "N/A",
                "earnings_date": "N/A"
            }
    except Exception as e:
        print(f"Error getting earnings data for {ticker}: {e}")
        return {
            "next_earnings": "N/A",
            "earnings_date": "N/A"
        }

def calculate_volatility(ticker: str) -> Dict[str, Any]:
    """Calculate volatility metrics for a stock"""
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="30d")
        
        if not hist.empty and len(hist) > 5:
            # Calculate daily returns
            hist['Returns'] = hist['Close'].pct_change()
            
            # Calculate annualized volatility
            daily_volatility = hist['Returns'].std()
            annualized_volatility = daily_volatility * (252 ** 0.5) * 100
            
            # Get volatility rating
            volatility_rating = get_volatility_rating(annualized_volatility)
            
            return {
                "annualized_volatility": round(annualized_volatility, 2),
                "volatility_rating": volatility_rating,
                "daily_volatility": round(daily_volatility * 100, 2)
            }
        else:
            return {
                "annualized_volatility": 0,
                "volatility_rating": "Unknown",
                "daily_volatility": 0
        }
    except Exception as e:
        print(f"Error calculating volatility for {ticker}: {e}")
        return {
            "annualized_volatility": 0,
            "volatility_rating": "Error",
            "daily_volatility": 0
        }

def get_volatility_rating(volatility: float) -> str:
    """Get volatility rating based on percentage"""
    if volatility > 30:
        return "High"
    elif volatility > 20:
        return "Moderate"
    elif volatility > 10:
        return "Low"
    else:
        return "Very Low"

@app.post("/api/stock-data")
async def get_stock_data_endpoint(request: StockRequest):
    """Alternative endpoint for stock data"""
    return await analyze_stock(request.ticker)

@app.get("/api/earnings/{ticker}")
async def get_earnings_data_endpoint(ticker: str):
    """Get earnings data for a stock"""
    return get_earnings_data(ticker) 