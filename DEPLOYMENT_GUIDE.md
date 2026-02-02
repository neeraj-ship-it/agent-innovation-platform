# 🚀 AMAIP Deployment Guide

## Deploy Kaise Karein?

### Option 1: Quick Deploy (Recommended)

#### Backend → Railway
```bash
# 1. Railway account banao: railway.app
# 2. Railway CLI install karo
npm install -g @railway/cli

# 3. Backend deploy karo
cd backend
railway login
railway init
railway up

# Railway automatically detect karega Node.js aur deploy karega
# Output: https://your-app.railway.app
```

#### Frontend → Vercel
```bash
# 1. Vercel account banao: vercel.com
# 2. Vercel CLI install karo
npm install -g vercel

# 3. Frontend deploy karo
cd frontend
vercel login
vercel

# Environment variable set karo:
# API_URL=https://your-backend.railway.app

# Output: https://your-app.vercel.app
```

### Option 2: Docker Deploy

#### Create Dockerfile for Backend
```dockerfile
# backend/Dockerfile
FROM node:18
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 4000
CMD ["npm", "start"]
```

#### Create Dockerfile for Frontend
```dockerfile
# frontend/Dockerfile
FROM node:18 AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "4000:4000"
    environment:
      - PORT=4000

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    environment:
      - API_URL=http://backend:4000
```

### Option 3: Cloud Platforms

#### AWS (Elastic Beanstalk)
```bash
# Backend deploy
cd backend
eb init
eb create amaip-backend
eb deploy

# Frontend deploy (S3 + CloudFront)
cd frontend
npm run build
aws s3 sync dist/ s3://your-bucket
```

#### Google Cloud (Cloud Run)
```bash
# Backend
cd backend
gcloud run deploy amaip-backend --source .

# Frontend
cd frontend
npm run build
gcloud app deploy
```

#### Heroku
```bash
# Backend
cd backend
heroku create amaip-backend
git push heroku main

# Frontend
cd frontend
heroku create amaip-frontend
git push heroku main
```

## Post-Deployment Setup

### 1. Update Frontend API URL
```javascript
// frontend/src/App.jsx
const API_URL = 'https://your-backend.railway.app'
```

### 2. Enable CORS on Backend
```javascript
// backend/src/server.js
// Already configured! ✅
app.use(cors({
  origin: ['https://your-frontend.vercel.app']
}))
```

### 3. Update Agent SDK
```python
# agents ko naya URL do
client = AMAIPClient(base_url="https://your-backend.railway.app")
```

### 4. Add Environment Variables
```bash
# Backend
PORT=4000
NODE_ENV=production

# Frontend
VITE_API_URL=https://your-backend.railway.app
```

## Testing Deployed App

```bash
# 1. Check backend health
curl https://your-backend.railway.app/health

# 2. Open frontend
open https://your-app.vercel.app

# 3. Run agent with new URL
python3 example-agent.py --url https://your-backend.railway.app
```

## Custom Domain (Optional)

### For Vercel (Frontend)
```bash
vercel domains add your-domain.com
# DNS mein CNAME add karo
```

### For Railway (Backend)
```bash
# Railway dashboard se custom domain add karo
api.your-domain.com → railway app
```

## Monitoring

### Backend Logs
```bash
# Railway
railway logs

# Heroku
heroku logs --tail
```

### Frontend Analytics
- Vercel Analytics (built-in)
- Google Analytics
- Plausible

## Security Checklist

✅ HTTPS enabled
✅ CORS configured properly
✅ Environment variables set
✅ Rate limiting (add if needed)
✅ Authentication (add if needed)

## Cost Estimate

- Railway: Free tier (500 hours/month)
- Vercel: Free tier (unlimited)
- Total: **FREE for starting!** 🎉

Deploy karne ke baad external agents actually aa sakenge!
