# 🚀 Production Deployment Guide

## Overview

Deploy your arXiv AI Research Summarizer to production with **Railway** (backend) and **Vercel** (frontend).

**Total Cost: FREE** 🎉

---

## 📋 Pre-deployment Checklist

- [x] Backend production-ready (Gunicorn, Procfile)
- [x] Environment configuration files created
- [ ] Claude API key ready
- [ ] GitHub repository created
- [ ] Railway account created
- [ ] Vercel account created

---

## 🔧 Step 1: Prepare Your Repository

### 1.1 Create GitHub Repository

```bash
# In your project root directory
git add .
git commit -m "Initial commit - arXiv AI Research Summarizer

🎯 Features:
- Fetch latest AI research papers from arXiv
- Generate AI summaries using Claude API
- Clean React frontend with responsive design
- Full-stack Flask + React application

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

# Create repo on GitHub and push
git remote add origin https://github.com/YOUR_USERNAME/arxiv-ai-summarizer.git
git branch -M main
git push -u origin main
```

---

## 🚂 Step 2: Deploy Backend to Railway

### 2.1 Sign Up & Connect Repository

1. Go to [Railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your `arxiv-ai-summarizer` repository
5. Choose **backend** folder as the root directory

### 2.2 Configure Environment Variables

In Railway dashboard, go to **Variables** tab and add:

```env
ANTHROPIC_API_KEY=your_claude_api_key_here
FLASK_ENV=production
FLASK_DEBUG=false
PORT=8000
```

### 2.3 Deploy

Railway will automatically:
- ✅ Detect Python project
- ✅ Install dependencies from `requirements.txt`
- ✅ Use `Procfile` to start Gunicorn server
- ✅ Provide you with a public URL like `https://arxiv-backend-production.up.railway.app`

**Expected build time:** 3-5 minutes

---

## ⚡ Step 3: Deploy Frontend to Vercel

### 3.1 Update Frontend Configuration

First, update the API URL in your frontend to point to your Railway backend:

```typescript
// In frontend/src/services/api.ts
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://your-railway-app.up.railway.app';
```

### 3.2 Sign Up & Deploy

1. Go to [Vercel.com](https://vercel.com)
2. Sign up with GitHub
3. Click "New Project"
4. Import your GitHub repository
5. Configure build settings:
   - **Framework Preset:** Create React App
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `build`

### 3.3 Add Environment Variables

In Vercel dashboard, go to **Settings** → **Environment Variables**:

```env
REACT_APP_API_URL=https://your-railway-backend.up.railway.app
```

### 3.4 Deploy

Vercel will:
- ✅ Build your React app
- ✅ Deploy to CDN
- ✅ Provide URL like `https://arxiv-ai-summarizer.vercel.app`

**Expected build time:** 2-3 minutes

---

## 🔗 Step 4: Configure CORS & Final Setup

### 4.1 Update Backend CORS

Your backend already has CORS enabled for all origins, which works for production. If you want to restrict it:

```python
# In backend/app/app.py
CORS(app, origins=["https://your-vercel-app.vercel.app"])
```

### 4.2 Test Your Production App

1. Visit your Vercel frontend URL
2. Try fetching papers - should work end-to-end
3. Check different categories and paper limits

---

## 📊 Production Monitoring

### Railway Backend Health Check
- URL: `https://your-railway-app.up.railway.app/health`
- Expected: `{"status": "healthy", ...}`

### API Test Endpoint
- URL: `https://your-railway-app.up.railway.app/api/test`
- Expected: `{"results": {"arxiv": true, "claude": true}}`

---

## 💰 Cost Breakdown

### Railway (Backend)
- **Free Tier**: $0/month
- **Limits**: 500 hours/month (enough for moderate usage)
- **Upgrade**: $5/month for unlimited

### Vercel (Frontend)
- **Free Tier**: $0/month
- **Limits**: 100GB bandwidth, unlimited sites
- **Upgrade**: $20/month for pro features

### Claude API
- **Pay-per-use**: ~$0.01-0.05 per 10 papers
- **Expected**: <$10/month for moderate usage

**Total: FREE to start, <$15/month for heavy usage**

---

## 🐛 Troubleshooting

### Backend Issues
- **500 Error**: Check Railway logs for API key issues
- **CORS Error**: Verify frontend is using correct backend URL
- **Slow Response**: Normal for first request (cold start)

### Frontend Issues
- **White Screen**: Check Vercel build logs
- **API Errors**: Verify REACT_APP_API_URL is set correctly
- **Build Failures**: Ensure frontend builds locally first

### Common Solutions
```bash
# Test backend locally with production settings
export FLASK_ENV=production
python run.py

# Test frontend with production API
export REACT_APP_API_URL=https://your-railway-app.up.railway.app
npm start
```

---

## 🚀 Go Live Commands

Run these commands to deploy:

```bash
# 1. Commit and push to GitHub
git add .
git commit -m "Production deployment ready"
git push

# 2. Railway will auto-deploy backend
# 3. Vercel will auto-deploy frontend
# 4. Update REACT_APP_API_URL in Vercel dashboard
# 5. Your app is LIVE! 🎉
```

---

## 🎯 Post-Deployment

### Share Your App
- **Frontend URL**: `https://your-app.vercel.app`
- **Features**: Latest AI research with Claude summaries
- **Categories**: AI, ML, Computer Vision, NLP, Robotics

### Future Enhancements
- [ ] Custom domain name
- [ ] Paper caching with Redis
- [ ] User favorites system
- [ ] Email digest subscriptions
- [ ] PDF text extraction

**Your arXiv AI Research Summarizer is now LIVE for the world to use!** 🌍✨