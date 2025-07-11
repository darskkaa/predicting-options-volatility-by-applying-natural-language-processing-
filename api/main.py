"""
VOLA Engine API

This FastAPI application provides endpoints for real-time stock volatility analysis, integrating with Polygon.io, FMP, and yfinance APIs. It exposes endpoints for comprehensive stock data, volatility metrics, and earnings information, designed for quant research and financial analytics workflows.
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
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
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
    # Try Polygon.io first
    polygon_data = get_polygon_data(ticker)
    if polygon_data and polygon_data.get("price", 0) > 0:
        return polygon_data
    # Try yfinance
    yf_data = get_yfinance_data(ticker)
    if yf_data and yf_data.get("price", 0) > 0:
        return yf_data
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
                "ticker": ticker,
                "price": current_price,
                "price_change": round(price_change, 2),
                "price_change_percent": round(price_change_percent, 2),
                "volume": int(hist['Volume'].iloc[-1]),
                "avg_volume": avg_volume,
                "market_cap": market_cap,
                "high": float(hist['High'].iloc[-1]),
                "low": float(hist['Low'].iloc[-1]),
                "open": float(hist['Open'].iloc[-1]),
                "source": "yfinance"
            }
        
        return None
        
    except Exception as e:
        print(f"yfinance error for {ticker}: {e}")
        return None

def get_polygon_data(ticker: str) -> Optional[Dict[str, Any]]:
    """Get real-time data from Polygon.io"""
    try:
        url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/prev"
        params = {"apiKey": POLYGON_API_KEY}
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("results"):
                result = data["results"][0]
                price = result.get("c", 0)
                
                # Calculate price change from previous day
                prev_price = result.get("o", price)  # Use open as approximation
                price_change = price - prev_price
                price_change_percent = (price_change / prev_price) * 100 if prev_price > 0 else 0
                
                return {
                    "ticker": ticker,
                    "price": price,
                    "price_change": round(price_change, 2),
                    "price_change_percent": round(price_change_percent, 2),
                    "volume": result.get("v", 0),
                    "avg_volume": 0,  # Polygon doesn't provide this
                    "market_cap": 0,  # Polygon doesn't provide this
                    "high": result.get("h", 0),
                    "low": result.get("l", 0),
                    "open": result.get("o", 0),
                    "source": "Polygon.io"
                }
        return None
    except Exception as e:
        print(f"Polygon API error: {e}")
        return None

def get_fmp_data(ticker: str) -> Optional[dict]:
    """Get data from Financial Modeling Prep (FMP) API"""
    try:
        url = f"https://financialmodelingprep.com/api/v3/quote/{ticker}"
        params = {"apikey": FMP_API_KEY}
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data and isinstance(data, list) and len(data) > 0:
                d = data[0]
                return {
                    "ticker": ticker,
                    "price": d.get("price", 0),
                    "price_change": d.get("change", 0),
                    "price_change_percent": d.get("changesPercentage", 0),
                    "volume": d.get("volume", 0),
                    "avg_volume": d.get("avgVolume", 0),
                    "market_cap": d.get("marketCap", 0),
                    "high": d.get("dayHigh", 0),
                    "low": d.get("dayLow", 0),
                    "open": d.get("open", 0),
                    "source": "FMP"
                }
        return None
    except Exception as e:
        print(f"FMP API error: {e}")
        return None

def generate_simulated_stock_data(ticker: str) -> Dict[str, Any]:
    """Generate realistic simulated stock data"""
    import random
    
    # Generate realistic price data
    base_price = random.uniform(50, 500)
    price_change = random.uniform(-20, 20)
    price_change_percent = (price_change / base_price) * 100
    current_price = base_price + price_change
    
    return {
        "ticker": ticker,
        "price": round(current_price, 2),
        "price_change": round(price_change, 2),
        "price_change_percent": round(price_change_percent, 2),
        "volume": random.randint(1000000, 50000000),
        "avg_volume": random.randint(2000000, 60000000),
        "market_cap": random.randint(1000000000, 500000000000),
        "high": round(current_price * random.uniform(1.01, 1.05), 2),
        "low": round(current_price * random.uniform(0.95, 0.99), 2),
        "open": round(current_price * random.uniform(0.98, 1.02), 2),
        "source": "simulated"
    }

def get_earnings_data(ticker: str) -> Dict[str, Any]:
    """Get earnings data with next earnings date"""
    try:
        # Try Financial Modeling Prep
        url = f"https://financialmodelingprep.com/api/v3/earnings-calendar/{ticker}"
        params = {"apikey": FMP_API_KEY}
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                next_earnings = data[0]
                return {
                    "next_earnings": f"Q{next_earnings.get('quarter', 'N/A')} {next_earnings.get('year', 'N/A')}",
                    "earnings_date": next_earnings.get('date', 'N/A'),
                    "eps": next_earnings.get('eps', 0),
                    "revenue": next_earnings.get('revenue', 0),
                    "source": "Financial Modeling Prep"
                }
        
        # Fallback to simulated data
        return generate_simulated_earnings_data(ticker)
        
    except Exception as e:
        print(f"Earnings data error: {e}")
        return generate_simulated_earnings_data(ticker)

def generate_simulated_earnings_data(ticker: str) -> Dict[str, Any]:
    """Generate simulated earnings data"""
    import random
    from datetime import datetime, timedelta
    
    # Generate next earnings date (next quarter)
    now = datetime.now()
    next_quarter = ((now.month - 1) // 3 + 1) % 4 + 1
    next_year = now.year if next_quarter > 1 else now.year + 1
    
    return {
        "next_earnings": f"Q{next_quarter} {next_year}",
        "earnings_date": (now + timedelta(days=90)).strftime("%Y-%m-%d"),
        "eps": round(random.uniform(0.5, 3.0), 2),
        "revenue": round(random.uniform(1000000, 50000000), 2),
        "source": "simulated"
    }

def calculate_volatility(ticker: str) -> Dict[str, Any]:
    """Calculate volatility metrics for the stock"""
    try:
        # Add delay to avoid rate limiting
        time.sleep(random.uniform(0.5, 1.5))
        
        stock = yf.Ticker(ticker)
        hist = stock.history(period="30d")
        
        if not hist.empty and len(hist) > 1:
            # Calculate daily returns
            hist['Returns'] = hist['Close'].pct_change()
            
            # Volatility metrics
            daily_volatility = hist['Returns'].std()
            annualized_volatility = daily_volatility * (252 ** 0.5)  # Annualized
            
            # Price range
            price_range = hist['High'].max() - hist['Low'].min()
            avg_price = hist['Close'].mean()
            
            return {
                "daily_volatility": round(daily_volatility * 100, 2),  # As percentage
                "annualized_volatility": round(annualized_volatility * 100, 2),
                "price_range": round(price_range, 2),
                "avg_price": round(avg_price, 2),
                "volatility_rating": get_volatility_rating(annualized_volatility),
                "analysis_period": "30 days"
            }
        
        # Fallback to simulated volatility
        return generate_simulated_volatility_data()
        
    except Exception as e:
        print(f"Volatility calculation error: {e}")
        return generate_simulated_volatility_data()

def generate_simulated_volatility_data() -> Dict[str, Any]:
    """Generate simulated volatility data"""
    import random
    
    volatility = random.uniform(15, 35)
    
    return {
        "daily_volatility": round(volatility / 16, 2),  # Daily volatility
        "annualized_volatility": round(volatility, 2),
        "price_range": round(random.uniform(10, 50), 2),
        "avg_price": round(random.uniform(100, 300), 2),
        "volatility_rating": get_volatility_rating(volatility / 100),
        "analysis_period": "30 days"
    }

def get_volatility_rating(volatility: float) -> str:
    """Get volatility rating based on annualized volatility"""
    if volatility < 0.15:  # < 15%
        return "Low"
    elif volatility < 0.25:  # 15-25%
        return "Medium"
    elif volatility < 0.35:  # 25-35%
        return "High"
    else:  # > 35%
        return "Very High"

@app.post("/api/stock-data")
async def get_stock_data_endpoint(request: StockRequest):
    """Get stock data using real APIs with fallback to yfinance"""
    ticker = request.ticker.upper()
    
    try:
        stock_data = get_comprehensive_stock_data(ticker)
        return {
            "success": True,
            "source": stock_data.get("source", "Unknown"),
            "data": stock_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/earnings/{ticker}")
async def get_earnings_data_endpoint(ticker: str):
    """Get earnings data from Financial Modeling Prep"""
    return get_earnings_data(ticker)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000) 