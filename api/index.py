"""
VOLA Engine API - Entry point for Vercel deployment

This file serves as the entry point for Vercel serverless functions.
It imports the FastAPI app from main.py and adds additional endpoints.
"""
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(__file__))

try:
    from main import app
except ImportError as e:
    print(f"Error importing from main.py: {e}")
    # Create a minimal app if import fails
    from fastapi import FastAPI
    app = FastAPI(title="VOLA Engine API", version="1.0.0")

from fastapi import HTTPException
from datetime import datetime
import random

# Add sentiment analysis endpoint
@app.get("/api/sentiment/{ticker}")
async def get_sentiment_analysis(ticker: str):
    """Get sentiment analysis for a stock ticker"""
    ticker = ticker.upper()
    
    try:
        # For now, return mock sentiment data
        # In a real implementation, you would integrate with a sentiment analysis service
        # like Google Cloud Natural Language API, AWS Comprehend, or a custom NLP model
        
        # Mock sentiment data based on stock performance
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
        
        # Randomly select sentiment (in real implementation, this would be based on actual analysis)
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

# Add a simple test endpoint
@app.get("/api/test")
def test_endpoint():
    return {"message": "API is working!", "status": "success"}

# Add a health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Export the app for Vercel
app.debug = False 