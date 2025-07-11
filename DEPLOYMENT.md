# VOLA Engine - Vercel Deployment Guide

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Account**: Your code should be in a GitHub repository
3. **API Keys**: You'll need API keys for:
   - Polygon.io (for real-time stock data)
   - Financial Modeling Prep (FMP) (for additional financial data)

## Step 1: Prepare Your Repository

Make sure your code is pushed to GitHub with the following structure:
```
vola-engine/
├── api/
│   ├── main.py
│   ├── requirements.txt
│   └── runtime.txt
├── app/
│   ├── package.json
│   ├── next.config.js
│   └── src/
├── vercel.json
└── README.md
```

## Step 2: Deploy to Vercel

### Option A: Deploy via Vercel Dashboard

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click "New Project"
3. Import your GitHub repository
4. Configure the project:
   - **Framework Preset**: Other
   - **Root Directory**: `vola-engine`
   - **Build Command**: Leave empty (Vercel will auto-detect)
   - **Output Directory**: Leave empty

### Option B: Deploy via Vercel CLI

1. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Navigate to your project directory:
   ```bash
   cd vola-engine
   ```

3. Deploy:
   ```bash
   vercel
   ```

## Step 3: Configure Environment Variables

In your Vercel dashboard:

1. Go to your project settings
2. Navigate to "Environment Variables"
3. Add the following variables:

```
POLYGON_API_KEY=your_polygon_api_key_here
FMP_API_KEY=your_fmp_api_key_here
```

## Step 4: Get API Keys

### Polygon.io API Key
1. Sign up at [polygon.io](https://polygon.io)
2. Get your API key from the dashboard
3. Add it to Vercel environment variables

### Financial Modeling Prep (FMP) API Key
1. Sign up at [financialmodelingprep.com](https://financialmodelingprep.com)
2. Get your API key from the dashboard
3. Add it to Vercel environment variables

## Step 5: Test Your Deployment

Once deployed, your app will be available at:
- Frontend: `https://your-project-name.vercel.app`
- Backend API: `https://your-project-name.vercel.app/api/`

Test the API endpoints:
- `https://your-project-name.vercel.app/api/analyze/AAPL`
- `https://your-project-name.vercel.app/api/health`

## Troubleshooting

### Common Issues:

1. **Build Errors**: Make sure all dependencies are in `requirements.txt`
2. **API Errors**: Verify your API keys are correctly set in Vercel
3. **CORS Issues**: The backend is configured to allow all origins in production
4. **Timeout Issues**: Vercel has a 10-second timeout limit for serverless functions

### Environment Variables Not Working:
- Make sure to redeploy after adding environment variables
- Check that variable names match exactly (case-sensitive)

### API Rate Limits:
- Polygon.io has rate limits on free tier
- Consider upgrading if you hit limits

## File Structure for Vercel

Your `vercel.json` is configured to:
- Serve the Next.js frontend from `/app`
- Route API calls to `/api/*` to the FastAPI backend
- Handle CORS automatically

## Monitoring

- Check Vercel dashboard for deployment status
- Monitor function logs in Vercel dashboard
- Set up alerts for API errors

## Custom Domain (Optional)

1. Go to your Vercel project settings
2. Navigate to "Domains"
3. Add your custom domain
4. Configure DNS settings as instructed

## Performance Optimization

- The backend uses serverless functions (15MB limit)
- Consider caching frequently requested data
- Monitor function execution times
- Optimize API calls to reduce latency

## Security Notes

- API keys are stored securely in Vercel environment variables
- CORS is configured for production
- All API calls are logged for monitoring
- Consider adding rate limiting for production use 