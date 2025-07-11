# VOLA Engine - Vercel Deployment Guide

This guide covers deploying the VOLA Engine to Vercel, a financial analysis tool with FastAPI backend and Next.js frontend.

## Deployment Overview

Deploy your entire VOLA Engine application (frontend + backend) to Vercel in one deployment.

## Prerequisites

1. **API Keys**: Get free API keys from:
   - [Polygon.io](https://polygon.io/) (free tier available)
   - [Financial Modeling Prep](https://financialmodelingprep.com/) (free tier available)

2. **GitHub Account**: For version control and deployment

3. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)

## Vercel Deployment

### Step 1: Prepare Repository
```bash
# Ensure your code is pushed to GitHub
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

### Step 2: Deploy to Vercel

1. **Go to Vercel Dashboard**: Visit [vercel.com/dashboard](https://vercel.com/dashboard)

2. **Import Repository**:
   - Click "New Project"
   - Import your GitHub repository
   - Vercel will automatically detect the Next.js app

3. **Configure Environment Variables**:
   - Go to Project Settings → Environment Variables
   - Add your API keys:
     - `POLYGON_API_KEY`: Your Polygon.io API key
     - `FMP_API_KEY`: Your Financial Modeling Prep API key

4. **Deploy**:
   - Click "Deploy"
   - Vercel will build and deploy your app

### Step 3: Verify Deployment

1. **Check Build Logs**: Monitor the build process in Vercel dashboard
2. **Test API Endpoints**: Visit `https://your-app.vercel.app/api/analyze/AAPL`
3. **Test Frontend**: Visit your Vercel URL to see the VOLA Engine interface

## Local Development

### Backend (FastAPI)
```bash
cd vola-engine/api
pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Frontend (Next.js)
```bash
cd vola-engine/app
npm install
npm run dev
```

## Environment Variables

Set these in Vercel dashboard:

- `POLYGON_API_KEY`: Your Polygon.io API key
- `FMP_API_KEY`: Your Financial Modeling Prep API key

## Troubleshooting

### Common Issues

1. **Python Dependencies**: Vercel automatically installs Python dependencies
2. **API Key Issues**: Ensure environment variables are set correctly
3. **Build Failures**: Check Vercel build logs for specific errors

### Support

- **Vercel Documentation**: [vercel.com/docs](https://vercel.com/docs)
- **Python on Vercel**: [vercel.com/docs/functions/serverless-functions/runtimes/python](https://vercel.com/docs/functions/serverless-functions/runtimes/python)

## Features

- **Full-Stack Deployment**: Both frontend and backend on Vercel
- **Automatic Scaling**: Vercel handles traffic spikes
- **Global CDN**: Fast loading worldwide
- **Serverless Functions**: Python backend runs as serverless functions
- **Automatic HTTPS**: SSL certificates included
- **Custom Domains**: Add your own domain

Your VOLA Engine will be live at `https://your-app.vercel.app` after deployment. 