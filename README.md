# Volatility Linguistics Arbitrage Engine (VOLA)

A financial analysis tool for stock volatility, earnings, and market metrics. **Made by Adil.**

## 🎯 Overview

VOLA provides comprehensive stock analysis, volatility calculations, earnings date detection, and market metrics. Built for clarity, transparency, and reliability—no AI or Copilot authorship involved.

## ✨ Features

### 🔍 **Core Analysis**
- **Real-time stock data analysis** using yfinance
- **Volatility calculation** with historical comparisons (3m, 6m periods)
- **Earnings date detection** and impact assessment
- **Market metrics** (market cap, volume, sector analysis)
- **Interactive data visualization**
- **Responsive design**

## 🛠️ Tech Stack

### Backend
- **FastAPI** - High-performance web framework
- **Python 3.11+** - Core language
- **yfinance** - Stock data retrieval
- **Pandas/NumPy** - Data processing

### Frontend
- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Framer Motion** - Animations
- **Recharts** - Data visualization

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
- `GET /earnings/{ticker}` - Earnings date and info

### Health & Info
- `GET /` - API information and features
- `GET /health` - Health check

## 🎨 Usage

1. **Enter a stock symbol** (e.g., AAPL, TSLA, META)
2. **View comprehensive analysis** including:
   - Current volatility metrics
   - Historical volatility comparison
   - Earnings and market metrics
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
- **Earnings Data**: Upcoming and historical earnings
- **Market Context**: Sector, industry, and market cap analysis

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

*VOLA Engine: Built for clarity and precision in volatility analysis. No AI, no Copilot, just Adil.* 