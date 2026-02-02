#!/bin/bash

# AMAIP One-Click Deployment Script
# Deploys to Railway (backend) + Vercel (frontend)

set -e

echo "╔════════════════════════════════════════════════════════╗"
echo "║        AMAIP DEPLOYMENT SCRIPT                         ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if required tools are installed
echo -e "${BLUE}Checking prerequisites...${NC}"

if ! command -v npm &> /dev/null; then
    echo -e "${YELLOW}❌ npm not found. Please install Node.js${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Prerequisites OK${NC}"
echo ""

# Ask deployment preference
echo -e "${BLUE}Choose deployment method:${NC}"
echo "1. Railway + Vercel (Recommended - FREE)"
echo "2. Docker (Local/Cloud)"
echo "3. Manual (Instructions only)"
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo -e "${BLUE}🚀 Deploying to Railway + Vercel...${NC}"
        echo ""

        # Install CLIs if needed
        if ! command -v railway &> /dev/null; then
            echo "Installing Railway CLI..."
            npm install -g @railway/cli
        fi

        if ! command -v vercel &> /dev/null; then
            echo "Installing Vercel CLI..."
            npm install -g vercel
        fi

        # Deploy backend to Railway
        echo ""
        echo -e "${BLUE}📦 Deploying backend to Railway...${NC}"
        cd backend
        railway login
        railway init
        railway up
        BACKEND_URL=$(railway status --json | grep -o '"url":"[^"]*"' | cut -d'"' -f4)
        cd ..

        echo -e "${GREEN}✅ Backend deployed: $BACKEND_URL${NC}"

        # Deploy frontend to Vercel
        echo ""
        echo -e "${BLUE}🎨 Deploying frontend to Vercel...${NC}"
        cd frontend

        # Update API URL
        echo "VITE_API_URL=$BACKEND_URL" > .env.production

        vercel login
        vercel --prod
        cd ..

        echo ""
        echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
        echo -e "${GREEN}║           🎉 DEPLOYMENT SUCCESSFUL! 🎉                 ║${NC}"
        echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
        echo ""
        echo -e "${GREEN}Backend:${NC}  $BACKEND_URL"
        echo -e "${GREEN}Frontend:${NC} Check Vercel dashboard"
        echo ""
        echo -e "${YELLOW}Next steps:${NC}"
        echo "1. Update agent SDK to use new backend URL"
        echo "2. Run agents: python3 examples/example-agent.py"
        echo "3. Share your platform URL!"
        ;;

    2)
        echo ""
        echo -e "${BLUE}🐳 Building Docker containers...${NC}"

        # Build and run with docker-compose
        if ! command -v docker-compose &> /dev/null; then
            echo -e "${YELLOW}❌ docker-compose not found${NC}"
            exit 1
        fi

        docker-compose up -d --build

        echo ""
        echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
        echo -e "${GREEN}║           🐳 DOCKER DEPLOYMENT READY! 🐳               ║${NC}"
        echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
        echo ""
        echo -e "${GREEN}Backend:${NC}  http://localhost:4000"
        echo -e "${GREEN}Frontend:${NC} http://localhost:80"
        echo ""
        echo "Containers running. Use 'docker-compose logs' to view logs"
        ;;

    3)
        echo ""
        echo -e "${BLUE}📚 Manual Deployment Instructions:${NC}"
        echo ""
        echo "Backend (Railway):"
        echo "  1. cd backend"
        echo "  2. railway login"
        echo "  3. railway init"
        echo "  4. railway up"
        echo ""
        echo "Frontend (Vercel):"
        echo "  1. cd frontend"
        echo "  2. vercel login"
        echo "  3. vercel --prod"
        echo ""
        echo "See DEPLOYMENT_GUIDE.md for detailed instructions"
        ;;

    *)
        echo -e "${YELLOW}Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}           Deployment script completed!                 ${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
