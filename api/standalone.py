"""
VOLA Engine API - Standalone version for Vercel deployment

This is a standalone version that includes all necessary endpoints
without depending on main.py, in case there are import issues.
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
    allow_origins=["*"],  # Allow all origins for Vercel
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

@app.get("/api/test")
def test_endpoint():
    return {"message": "API is working!", "status": "success"}

def format_large_number(num: float) -> str:
    if num >= 1e12:
        return f"{num / 1e12:.1f}T"
    if num >= 1e9:
        return f"{num / 1e9:.1f}B"
    if num >= 1e6:
        return f"{num / 1e6:.1f}M"
    if num >= 1e3:
        return f"{num / 1e3:.1f}K"
    return str(num)

@app.get("/api/analyze/{ticker}")
async def analyze_stock(ticker: str):
    """Analyze any stock ticker with comprehensive data"""
    ticker = ticker.upper()
    
    try:
        # Get stock data using yfinance
        stock = yf.Ticker(ticker)
        hist = stock.history(period="5d")
        
        if hist.empty:
            raise HTTPException(status_code=404, detail=f"No data found for {ticker}")
        
        current_price = float(hist['Close'].iloc[-1])
        prev_price = float(hist['Close'].iloc[-2])
        price_change = current_price - prev_price
        price_change_percent = (price_change / prev_price) * 100 if prev_price > 0 else 0
        
        # Get additional info
        try:
            info = stock.info
            market_cap = int(info.get('marketCap', 0))
            avg_volume = int(info.get('averageVolume', 0))
        except:
            market_cap = 0
            avg_volume = 0
        
        # Calculate volatility
        try:
            hist_30d = stock.history(period="30d")
            if not hist_30d.empty and len(hist_30d) > 5:
                hist_30d['Returns'] = hist_30d['Close'].pct_change()
                daily_volatility = hist_30d['Returns'].std()
                annualized_volatility = daily_volatility * (252 ** 0.5) * 100
            else:
                annualized_volatility = 0
        except:
            annualized_volatility = 0
        
        # Get volatility rating
        if annualized_volatility > 30:
            volatility_rating = "High"
        elif annualized_volatility > 20:
            volatility_rating = "Moderate"
        elif annualized_volatility > 10:
            volatility_rating = "Low"
        else:
            volatility_rating = "Very Low"
        
        return {
            "success": True,
            "ticker": ticker,
            "current_price": current_price,
            "price_change": price_change,
            "price_change_percent": price_change_percent,
            "market_cap": market_cap,
            "volume": int(hist['Volume'].iloc[-1]),
            "avg_volume": avg_volume,
            "high": float(hist['High'].iloc[-1]),
            "low": float(hist['Low'].iloc[-1]),
            "open": float(hist['Open'].iloc[-1]),
            "volatility_30d": round(annualized_volatility, 2),
            "volatility_rating": volatility_rating,
            "next_earnings": "N/A",
            "earnings_date": "N/A",
            "data_source": "Yahoo Finance",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
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
            "timestamp": datetime.now().isoformat()
        }

@app.get("/api/sentiment/{ticker}")
async def get_sentiment_analysis(ticker: str):
    """Get sentiment analysis for a stock ticker"""
    ticker = ticker.upper()
    
    try:
        # Mock sentiment data
        sentiment_options = [
            {
                "overall_sentiment": "Positive",
                "sentiment_score": 0.75,
                "key_phrases": ["strong performance", "growth potential", "market leader"],
                "risk_indicators": []
            },
            {
                "overall_sentiment": "Neutral",
                "sentiment_score": 0.50,
                "key_phrases": ["stable performance", "market average", "steady growth"],
                "risk_indicators": ["moderate volatility"]
            },
            {
                "overall_sentiment": "Negative",
                "sentiment_score": 0.25,
                "key_phrases": ["declining performance", "market concerns", "volatility"],
                "risk_indicators": ["high volatility", "earnings risk"]
            }
        ]
        
        sentiment_data = random.choice(sentiment_options)
        
        return {
            "success": True,
            "ticker": ticker,
            "overall_sentiment": sentiment_data["overall_sentiment"],
            "sentiment_score": sentiment_data["sentiment_score"],
            "key_phrases": sentiment_data["key_phrases"],
            "risk_indicators": sentiment_data["risk_indicators"],
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "success": False,
            "ticker": ticker,
            "error": f"Sentiment analysis failed: {str(e)}",
            "overall_sentiment": "Unknown",
            "sentiment_score": 0.0,
            "key_phrases": [],
            "risk_indicators": [],
            "timestamp": datetime.now().isoformat()
        }

# Export the app for Vercel
app.debug = False 