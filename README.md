# Volatility Linguistics Arbitrage Engine (VOLA)

A sophisticated financial analysis tool that predicts stock volatility through earnings call transcript analysis and NLP-powered sentiment analysis. Built by Adil.

## 🎯 Overview

VOLA leverages natural language processing and machine learning techniques to analyze earnings call transcripts and predict potential stock volatility. By examining linguistic patterns, sentiment, and key financial indicators, the engine provides valuable insights for investment decisions.

## ✨ Features

### 🔍 **Core Analysis**
- **Real-time stock data analysis** using yfinance
- **Volatility calculation** with historical comparisons (3m, 6m periods)
- **Earnings date detection** and impact assessment
- **Market metrics** (market cap, volume, sector analysis)

### 🧠 **NLP-Powered Features**
- **Sentiment analysis** using VADER and TextBlob
- **Earnings call transcript analysis** with key phrase extraction
- **Risk indicator detection** from financial language
- **Key topic identification** from earnings calls
- **Analyst question analysis** for deeper insights

### 📊 **Advanced Features**
- **Volatility prediction** based on sentiment and trends
- **Interactive data visualization** with Recharts
- **Real-time API integration** with comprehensive error handling
- **Responsive design** with modern glassmorphism UI

## 🛠️ Tech Stack

### Backend
- **FastAPI** - High-performance web framework
- **Python 3.11+** - Core language
- **yfinance** - Stock data retrieval
- **NLTK** - Natural language processing
- **TextBlob** - Sentiment analysis
- **scikit-learn** - Machine learning utilities
- **Pandas/NumPy** - Data processing

### Frontend
- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Framer Motion** - Animations
- **Recharts** - Data visualization
- **React Query** - Data fetching

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- npm or yarn

### Installation

1. **Clone and navigate to the project:**
   ```bash
   cd vola-engine
   ```

2. **Run the startup script:**
   ```bash
   python start_vola.py
   ```
   
   This will:
   - Install all backend dependencies
   - Install frontend dependencies
   - Start the backend server

3. **Start the frontend (in a new terminal):**
   ```bash
   cd app
   npm run dev
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://127.0.0.1:8000
   - API Documentation: http://127.0.0.1:8000/docs

## 📡 API Endpoints

### Core Analysis
- `GET /analyze/{ticker}` - Comprehensive stock analysis
- `GET /sentiment/{ticker}` - NLP sentiment analysis
- `GET /transcript/{ticker}` - Earnings call transcript analysis
- `GET /predict/{ticker}` - Volatility prediction

### Health & Info
- `GET /` - API information and features
- `GET /health` - Health check

## 🎨 Usage

1. **Enter a stock symbol** (e.g., AAPL, TSLA, META)
2. **View comprehensive analysis** including:
   - Current volatility metrics
   - Historical volatility comparison
   - Sentiment analysis from earnings calls
   - Risk indicators and key phrases
   - Market metrics and trends

3. **Explore the data** through interactive charts and visualizations

## 🔧 Development

### Backend Development
```bash
cd api
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Development
```bash
cd app
npm install
npm run dev
```

### API Testing
Visit http://127.0.0.1:8000/docs for interactive API documentation.

## 📊 Sample Analysis

The VOLA Engine provides detailed analysis including:

- **Volatility Metrics**: Current, 3-month, and 6-month volatility comparisons
- **Sentiment Analysis**: Overall sentiment score and breakdown
- **Key Phrases**: Important terms extracted from earnings calls
- **Risk Indicators**: Potential volatility triggers
- **Market Context**: Sector, industry, and market cap analysis

## 🔮 Future Enhancements

- [ ] Real earnings call transcript integration
- [ ] Advanced ML models for volatility prediction
- [ ] Real-time news sentiment analysis
- [ ] Portfolio-level analysis
- [ ] Advanced charting and technical indicators
- [ ] Machine learning model training pipeline

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details

## 👨‍💻 Author

**Adil** - Financial Technology Developer

---

*VOLA Engine: Where Linguistics Meets Volatility Analysis* 🚀 