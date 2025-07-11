# VOLA Engine

Advanced NLP-powered stock volatility analysis platform built with FastAPI and Next.js, deployed on Netlify.

## Features

- **Real-time Stock Analysis**: Get comprehensive stock data with volatility metrics
- **Multi-Source Data**: Integrates with Polygon.io, FMP, and yfinance APIs
- **Volatility Linguistics**: Advanced NLP analysis of stock market sentiment
- **Interactive Charts**: Beautiful visualizations with Recharts
- **Responsive Design**: Modern UI with Tailwind CSS and Framer Motion
- **API-First Architecture**: RESTful API for quant research workflows
- **Netlify Deployment**: Full-stack deployment on Netlify

## Tech Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **yfinance**: Yahoo Finance data integration
- **Polygon.io**: Real-time market data
- **Financial Modeling Prep**: Additional financial metrics
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first CSS framework
- **Framer Motion**: Smooth animations
- **Recharts**: Interactive data visualizations
- **SWR**: Data fetching and caching

## Installation

### Prerequisites
- Node.js 18+ 
- Python 3.11+
- Git

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/vola-engine.git
   cd vola-engine
   ```

2. **Install backend dependencies**
   ```bash
   cd api
   pip install -r requirements.txt
   ```

3. **Install frontend dependencies**
   ```bash
   cd ../app
   npm install
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file in api directory
   echo "POLYGON_API_KEY=your_polygon_key_here" > api/.env
   echo "FMP_API_KEY=your_fmp_key_here" >> api/.env
   ```

5. **Run the development servers**
   ```bash
   # Terminal 1: Backend
   cd api
   uvicorn main:app --reload --host 127.0.0.1 --port 8000
   
   # Terminal 2: Frontend
   cd app
   npm run dev
   ```

6. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://127.0.0.1:8000
   - API Docs: http://127.0.0.1:8000/docs

## Deployment

### Netlify Deployment
Deploy your entire application (frontend + backend) to Netlify in one deployment.

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Netlify deployment"
   git push origin main
   ```

2. **Deploy to Netlify**
   - Go to [netlify.com](https://netlify.com)
   - Connect your GitHub repository
   - Configure build settings:
     - **Base directory**: Leave empty (root)
     - **Build command**: `pip install -r api/requirements.txt && cd app && npm install && npm run build`
     - **Publish directory**: `app/out`

3. **Add Environment Variables**
   - Go to Site settings → Environment variables
   - Add: `POLYGON_API_KEY` and `FMP_API_KEY`

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment instructions.

## Configuration

### Environment Variables

#### Backend (api/.env)
```bash
POLYGON_API_KEY=your_polygon_key_here
FMP_API_KEY=your_fmp_key_here
```

### API Keys

Get free API keys from:
- [Polygon.io](https://polygon.io/) - Real-time market data
- [Financial Modeling Prep](https://financialmodelingprep.com/) - Financial metrics

## API Endpoints

### Core Endpoints
- `GET /analyze/{ticker}` - Comprehensive stock analysis
- `GET /health` - Health check
- `GET /` - API status

### Response Format
```json
{
  "success": true,
  "ticker": "AAPL",
  "current_price": 150.25,
  "price_change": 2.50,
  "price_change_percent": 1.67,
  "market_cap": 2500000000000,
  "volume": 50000000,
  "volatility_30d": 18.5,
  "volatility_rating": "Moderate",
  "next_earnings": "2024-01-25",
  "analysis_summary": "AAPL is currently trading at $150.25 with a moderate volatility of 18.5%..."
}
```

## Usage

1. **Search for a stock** by entering its ticker symbol (e.g., AAPL, TSLA, META)
2. **View real-time data** including price, volume, and market cap
3. **Analyze volatility** with 30-day metrics and ratings
4. **Check earnings** for upcoming earnings dates
5. **Explore charts** showing volatility trends and price movements

## Development

### Project Structure
```
vola-engine/
├── api/                 # FastAPI backend (Netlify Functions)
│   ├── main.py         # Main application
│   ├── requirements.txt # Python dependencies
│   └── runtime.txt     # Python version
├── app/                # Next.js frontend
│   ├── src/
│   │   └── app/        # App Router pages
│   ├── package.json    # Node.js dependencies
│   └── next.config.js  # Next.js configuration
├── netlify.toml        # Netlify deployment config
└── README.md
```

### Development Commands

```bash
# Backend development
cd api
uvicorn main:app --reload --host 127.0.0.1 --port 8000

# Frontend development
cd app
npm run dev

# Build for production
cd app
npm run build

# Export static site (for Netlify)
cd app
npm run export
```

## Testing

### API Testing
```bash
# Health check
curl http://localhost:8000/health

# Stock analysis
curl http://localhost:8000/analyze/AAPL
```

### Frontend Testing
- Open http://localhost:3000
- Search for different stock symbols
- Test responsive design on different screen sizes

## Performance

- **Backend**: FastAPI with async/await for high concurrency
- **Frontend**: Next.js with static generation and client-side caching
- **Data**: Multi-source fallback for reliable data access
- **Caching**: SWR for intelligent data fetching and caching
- **Netlify**: Functions with 10-second timeout, optimized for speed

## Security

- **API Keys**: Stored securely in environment variables
- **CORS**: Configured for production domains
- **Rate Limiting**: Built-in protection against abuse
- **Error Handling**: Comprehensive error management

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Polygon.io](https://polygon.io/) for real-time market data
- [Financial Modeling Prep](https://financialmodelingprep.com/) for financial metrics
- [yfinance](https://github.com/ranaroussi/yfinance) for Yahoo Finance integration
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [Next.js](https://nextjs.org/) for the React framework
- [Tailwind CSS](https://tailwindcss.com/) for the utility-first CSS framework
- [Netlify](https://netlify.com/) for the deployment platform

## Support

- **Documentation**: See [DEPLOYMENT.md](./DEPLOYMENT.md) for deployment guides
- **Issues**: Report bugs and feature requests on GitHub
- **Discussions**: Join the community discussions

---

**Built with ❤️ for quantitative finance and algorithmic trading research.** 