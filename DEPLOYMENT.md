# VOLA Engine - Netlify Deployment Guide

This guide covers deploying the VOLA Engine to Netlify, a financial analysis tool with FastAPI backend and Next.js frontend.

## Deployment Overview

Deploy your entire VOLA Engine application (frontend + backend) to Netlify in one deployment.

## Prerequisites

1. **API Keys**: Get free API keys from:
   - [Polygon.io](https://polygon.io/) (free tier available)
   - [Financial Modeling Prep](https://financialmodelingprep.com/) (free tier available)

2. **GitHub Account**: For version control and deployment

3. **Netlify Account**: Sign up at [netlify.com](https://netlify.com)

## Netlify Deployment

### Step 1: Prepare Repository
```bash
# Ensure your code is pushed to GitHub
git add .
git commit -m "Prepare for Netlify deployment"
git push origin main
```

### Step 2: Deploy to Netlify
1. Go to [netlify.com](https://netlify.com)
2. Sign up/Login with GitHub
3. Click "New site from Git"
4. Select your GitHub repository
5. Configure build settings:
   - **Base directory**: Leave empty (root)
   - **Build command**: `pip install -r api/requirements.txt && cd app && npm install && npm run build`
   - **Publish directory**: `app/out`
6. Click "Deploy site"

### Step 3: Configure Environment Variables
In your Netlify site dashboard:
1. Go to Site settings → Environment variables
2. Add the following variables:
   ```
   POLYGON_API_KEY=your_polygon_key_here
   FMP_API_KEY=your_fmp_key_here
   ```

### Step 4: Configure Functions
1. Go to Site settings → Functions
2. Ensure the `api` directory is set as the functions directory
3. The backend will be available at `/.netlify/functions/api/`

**Result**: Your app will be available at `https://your-site.netlify.app`

## Testing Your Deployment

### Health Check
- Backend: `https://your-site.netlify.app/.netlify/functions/api/health`
- Should return: `{"status": "healthy", "timestamp": "..."}`

### API Test
- Test endpoint: `https://your-site.netlify.app/.netlify/functions/api/analyze/AAPL`
- Should return stock analysis data

### Frontend Test
- Visit your Netlify URL
- Search for a stock (e.g., AAPL, TSLA)
- Verify data loads correctly

## Troubleshooting

### Common Issues

1. **Build Failures**
   - Check that all dependencies are in `requirements.txt`
   - Verify Node.js version is 18+
   - Ensure Python version is 3.11+

2. **API Keys Not Working**
   - Verify API keys are correctly set in environment variables
   - Check API key permissions and rate limits
   - Test with a simple stock like AAPL

3. **Functions Not Working**
   - Check that the `api` directory is properly configured
   - Verify the function timeout settings
   - Check the function logs in Netlify dashboard

4. **CORS Errors**
   - The backend is configured to allow all origins
   - Check that API URLs are correct

### Debug Commands

```bash
# Test locally
cd api
uvicorn main:app --reload --host 127.0.0.1 --port 8000

cd app
npm run dev

# Check environment variables
echo $POLYGON_API_KEY
echo $FMP_API_KEY
```

## Performance Optimization

### For Netlify Deployment
- Functions have a 10-second timeout limit
- Use caching for frequently requested data
- Optimize API calls to reduce latency
- Consider using Netlify's edge functions for better performance

## Security Considerations

1. **API Keys**: Never commit API keys to version control
2. **Environment Variables**: Use Netlify's environment variable system
3. **CORS**: Configured for production domains
4. **Rate Limiting**: Implement rate limiting for API endpoints

## Monitoring

### Netlify Analytics
- Page view analytics
- Build and deployment monitoring
- Function execution logs
- Error tracking and alerting

## Next Steps

1. **Custom Domain**: Configure custom domain for production
2. **SSL Certificate**: Ensure HTTPS is enabled
3. **Monitoring**: Set up error tracking and analytics
4. **Scaling**: Plan for increased traffic and usage

## Project Structure

```
vola-engine/
├── api/                 # FastAPI backend (Netlify Functions)
│   ├── main.py         # Main application
│   └── requirements.txt # Python dependencies
├── app/                # Next.js frontend
│   ├── src/
│   │   └── app/        # App Router pages
│   ├── package.json    # Node.js dependencies
│   └── next.config.js  # Next.js configuration
├── netlify.toml        # Netlify deployment config
└── README.md
```

## Configuration Files

### netlify.toml
- Configures build settings
- Sets up API redirects
- Defines function directory

### next.config.js
- Static export configuration
- Unoptimized images for static deployment

### requirements.txt
- Python dependencies optimized for Netlify
- Lightweight packages for faster deployment

---

**Need Help?** Check the troubleshooting section or create an issue in the repository. 