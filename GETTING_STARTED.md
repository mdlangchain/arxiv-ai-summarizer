# Getting Started with arXiv AI Research Paper Summarizer

## Quick Setup Guide

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Create .env file with your API key
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 2. Get Claude API Key

1. Go to [Anthropic Console](https://console.anthropic.com)
2. Create an account or sign in
3. Generate an API key
4. Add it to your `.env` file:
   ```
   ANTHROPIC_API_KEY=your_actual_api_key_here
   ```

### 3. Start the Backend

```bash
cd backend
source venv/bin/activate
python run.py
```

The backend will start at `http://localhost:5000`

### 4. Start the Frontend

```bash
# In a new terminal
cd frontend
npm install  # if not already done
npm start
```

The frontend will start at `http://localhost:3000`

## Testing

### Test Backend APIs
```bash
# Health check
curl http://localhost:5000/health

# Test API connections
curl http://localhost:5000/api/test

# Get 5 AI papers
curl "http://localhost:5000/api/papers?limit=5&category=cs.AI"
```

### Run Python Tests
```bash
cd backend
source venv/bin/activate
python -m pytest tests/ -v
```

## Features

- **Fetch Papers**: Get latest papers from arXiv by category
- **AI Summaries**: Generate concise summaries using Claude
- **Categories**: Support for AI, ML, NLP, Computer Vision, and more
- **Mobile Friendly**: Responsive design for all devices
- **Direct Links**: Easy access to PDFs and arXiv pages

## Troubleshooting

### Common Issues

1. **Backend won't start**: Check that your `ANTHROPIC_API_KEY` is set in `.env`
2. **No papers loading**: Verify backend is running and accessible
3. **API errors**: Check your Claude API key quota and validity

### Error Messages

- **"Service unavailable"**: Backend couldn't initialize - check API key
- **"Failed to fetch papers"**: Frontend can't reach backend
- **"Summary generation failed"**: Claude API issue - check key/quota

## Next Steps

1. **Customize Categories**: Add more arXiv categories in the frontend
2. **Caching**: Add Redis for paper caching
3. **Favorites**: Allow users to save papers
4. **Export**: Add PDF/Markdown export functionality

## API Endpoints

- `GET /health` - Health check
- `GET /api/papers?limit=10&category=cs.AI` - Get papers with summaries
- `GET /api/paper/{id}` - Get specific paper with summary
- `GET /api/test` - Test API connections
- `POST /api/refresh` - Refresh cache (placeholder)