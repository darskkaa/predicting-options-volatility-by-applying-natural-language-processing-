# VOLA Engine

Advanced NLP-powered stock volatility analysis platform built with FastAPI and Next.js, deployed on Vercel.

## Features

- **Real-time Stock Analysis**: Get comprehensive stock data with volatility metrics
- **Multi-Source Data**: Integrates with Polygon.io, FMP, and yfinance APIs
- **Volatility Linguistics**: Advanced NLP analysis of stock market sentiment
- **Interactive Charts**: Beautiful visualizations with Recharts
- **Responsive Design**: Modern UI with Tailwind CSS and Framer Motion
- **API-First Architecture**: RESTful API for quant research workflows
- **Vercel Deployment**: Full-stack deployment on Vercel

## Tech Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **yfinance**: Yahoo Finance data integration
- **Polygon.io**: Real-time market data
- **Financial Modeling Prep**: Fundamental data
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first CSS framework
- **Framer Motion**: Smooth animations
- **Recharts**: Data visualization library
- **SWR**: Data fetching and caching

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- API keys from [Polygon.io](https://polygon.io/) and [Financial Modeling Prep](https://financialmodelingprep.com/)

### Local Development

1. **Clone Repository**
```bash
git clone https://github.com/your-username/vola-engine.git
cd vola-engine
```

2. **Backend Setup**
```bash
cd api
pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

3. **Frontend Setup**
```bash
cd app
npm install
npm run dev
```

4. **Environment Variables**
Create `.env` files in both `api/` and `app/` directories:
```bash
# api/.env
POLYGON_API_KEY=your_polygon_key_here
FMP_API_KEY=your_fmp_key_here

# app/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## API Endpoints

### Stock Analysis
- `GET /analyze/{ticker}` - Comprehensive stock analysis
- `GET /health` - Health check endpoint

### Response Format
```json
{
  "ticker": "AAPL",
  "price": 150.25,
  "change": 2.15,
  "change_percent": 1.45,
  "volume": 45000000,
  "market_cap": 2500000000000,
  "pe_ratio": 25.5,
  "volatility": 0.35,
  "sentiment": "bullish",
  "recommendation": "buy"
}
```

## Deployment

### Vercel Deployment

1. **Push to GitHub**
```bash
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

2. **Deploy to Vercel**
- Go to [vercel.com/dashboard](https://vercel.com/dashboard)
- Import your GitHub repository
- Configure environment variables
- Deploy

3. **Environment Variables**
Set in Vercel dashboard:
- `POLYGON_API_KEY`: Your Polygon.io API key
- `FMP_API_KEY`: Your Financial Modeling Prep API key

Your app will be live at `https://your-app.vercel.app`

## Project Structure

```
vola-engine/
├── api/                 # FastAPI backend
│   ├── main.py         # Main application
│   └── requirements.txt # Python dependencies
├── app/                # Next.js frontend
│   ├── src/
│   │   └── app/        # App Router pages
│   ├── package.json    # Node.js dependencies
│   └── next.config.js  # Next.js configuration
├── vercel.json         # Vercel deployment config
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

- **Documentation**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Issues**: Create an issue in the repository
- **Discussions**: Use GitHub Discussions for questions

---

Built with ❤️ for quantitative finance and algorithmic trading. 