#!/bin/bash

# AMAIP Demo Launcher - Start everything with one command!

echo "╔════════════════════════════════════════════════════════╗"
echo "║         AMAIP DEMO LAUNCHER                            ║"
echo "║    Start Backend + Frontend + Multiple Agents          ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -d "backend" ] || [ ! -d "frontend" ] || [ ! -d "examples" ]; then
    echo -e "${RED}❌ Error: Please run this script from the agent-innovation-platform directory${NC}"
    exit 1
fi

echo -e "${BLUE}🚀 Starting AMAIP Platform...${NC}"
echo ""

# Kill any existing processes on ports 4000 and 5173
echo -e "${YELLOW}Cleaning up existing processes...${NC}"
lsof -ti:4000 | xargs kill -9 2>/dev/null || true
lsof -ti:5173 | xargs kill -9 2>/dev/null || true
sleep 1

# Start Backend
echo -e "${BLUE}📦 Starting Backend Server...${NC}"
cd backend
npm start > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..
echo -e "${GREEN}✅ Backend starting on http://localhost:4000 (PID: $BACKEND_PID)${NC}"
sleep 3

# Start Frontend
echo -e "${BLUE}🎨 Starting Frontend UI...${NC}"
cd frontend
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..
echo -e "${GREEN}✅ Frontend starting on http://localhost:5173 (PID: $FRONTEND_PID)${NC}"
sleep 3

# Ask user which agents to launch
echo ""
echo -e "${BLUE}🤖 Choose agents to launch:${NC}"
echo "1. Basic Demo (3 agents)"
echo "2. Full Demo (6+ agents with personalities)"
echo "3. Competition Mode (5 competitive agents)"
echo "4. AI Orchestrator Mode (Orchestrator + 4 agents)"
echo "5. Custom (choose manually)"
read -p "Enter choice (1-5): " agent_choice

cd examples

case $agent_choice in
    1)
        echo -e "${BLUE}Launching Basic Demo...${NC}"
        python3 example-agent.py > ../agent1.log 2>&1 &
        python3 team-agent.py > ../agent2.log 2>&1 &
        python3 learning-agent.py > ../agent3.log 2>&1 &
        echo -e "${GREEN}✅ 3 agents launched${NC}"
        ;;

    2)
        echo -e "${BLUE}Launching Full Demo with Personalities...${NC}"
        python3 example-agent.py > ../agent1.log 2>&1 &
        python3 team-agent.py > ../agent2.log 2>&1 &
        python3 learning-agent.py > ../agent3.log 2>&1 &
        python3 personality-agent.py > ../agent4.log 2>&1 &
        sleep 2
        python3 personality-agent.py > ../agent5.log 2>&1 &
        python3 personality-agent.py > ../agent6.log 2>&1 &
        echo -e "${GREEN}✅ 6 agents launched (3 with unique personalities!)${NC}"
        ;;

    3)
        echo -e "${BLUE}Launching Competition Mode...${NC}"
        python3 competitive-game-agent.py > ../comp1.log 2>&1 &
        sleep 1
        python3 competitive-game-agent.py > ../comp2.log 2>&1 &
        sleep 1
        python3 competitive-game-agent.py > ../comp3.log 2>&1 &
        sleep 1
        python3 competitive-game-agent.py > ../comp4.log 2>&1 &
        sleep 1
        python3 competitive-game-agent.py > ../comp5.log 2>&1 &
        echo -e "${GREEN}✅ 5 competitive agents launched - Let the games begin!${NC}"
        ;;

    4)
        echo -e "${BLUE}Launching AI Orchestrator Mode...${NC}"
        python3 ai-orchestrator-agent.py > ../orchestrator.log 2>&1 &
        echo -e "${GREEN}✅ AI Orchestrator launched${NC}"
        sleep 2
        python3 example-agent.py > ../agent1.log 2>&1 &
        python3 team-agent.py > ../agent2.log 2>&1 &
        python3 learning-agent.py > ../agent3.log 2>&1 &
        python3 personality-agent.py > ../agent4.log 2>&1 &
        echo -e "${GREEN}✅ 4 worker agents launched${NC}"
        ;;

    5)
        echo -e "${BLUE}Available agents:${NC}"
        echo "  1. example-agent.py - Basic agent"
        echo "  2. team-agent.py - Team collaboration"
        echo "  3. learning-agent.py - Learning from experience"
        echo "  4. swarm-agent.py - Swarm coordinator"
        echo "  5. personality-agent.py - Personality-driven"
        echo "  6. competitive-game-agent.py - Competition mode"
        echo "  7. ai-orchestrator-agent.py - AI orchestrator"

        read -p "Enter agent numbers to launch (comma-separated, e.g., 1,2,3): " agents

        IFS=',' read -ra AGENT_NUMS <<< "$agents"
        for num in "${AGENT_NUMS[@]}"; do
            case $num in
                1) python3 example-agent.py > ../agent_$num.log 2>&1 & ;;
                2) python3 team-agent.py > ../agent_$num.log 2>&1 & ;;
                3) python3 learning-agent.py > ../agent_$num.log 2>&1 & ;;
                4) python3 swarm-agent.py > ../agent_$num.log 2>&1 & ;;
                5) python3 personality-agent.py > ../agent_$num.log 2>&1 & ;;
                6) python3 competitive-game-agent.py > ../agent_$num.log 2>&1 & ;;
                7) python3 ai-orchestrator-agent.py > ../agent_$num.log 2>&1 & ;;
            esac
            sleep 1
        done
        echo -e "${GREEN}✅ Custom agents launched${NC}"
        ;;

    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

cd ..

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║           🎉 AMAIP DEMO IS RUNNING! 🎉                 ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📍 Access Points:${NC}"
echo -e "   🖥️  Frontend:  ${GREEN}http://localhost:5173${NC}"
echo -e "   🔌 Backend:   ${GREEN}http://localhost:4000${NC}"
echo -e "   📊 Analytics: ${GREEN}http://localhost:4000/api/analytics/stats${NC}"
echo ""
echo -e "${BLUE}📋 Logs:${NC}"
echo -e "   Backend:  tail -f backend.log"
echo -e "   Frontend: tail -f frontend.log"
echo -e "   Agents:   tail -f agent*.log"
echo ""
echo -e "${BLUE}🛑 To stop all processes:${NC}"
echo -e "   ${YELLOW}kill $BACKEND_PID $FRONTEND_PID${NC}"
echo -e "   ${YELLOW}pkill -f 'python3.*agent'${NC}"
echo ""
echo -e "${YELLOW}💡 Tip: Open http://localhost:5173 in your browser to see the magic!${NC}"
echo ""
echo -e "${GREEN}Press Ctrl+C to stop the demo and clean up all processes${NC}"
echo ""

# Save PIDs for cleanup
echo $BACKEND_PID > .demo.pids
echo $FRONTEND_PID >> .demo.pids

# Wait for Ctrl+C
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Stopping AMAIP Demo...${NC}"

    # Kill backend and frontend
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true

    # Kill all Python agents
    pkill -f 'python3.*agent' 2>/dev/null || true

    # Clean up
    rm -f .demo.pids

    echo -e "${GREEN}✅ All processes stopped${NC}"
    echo -e "${BLUE}Thanks for using AMAIP! 🚀${NC}"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Keep script running
echo -e "${BLUE}Demo is running... Press Ctrl+C to stop${NC}"
while true; do
    sleep 10

    # Check if processes are still running
    if ! ps -p $BACKEND_PID > /dev/null 2>&1; then
        echo -e "${RED}⚠️  Backend process died unexpectedly${NC}"
        echo -e "${YELLOW}Check backend.log for errors${NC}"
        cleanup
    fi

    if ! ps -p $FRONTEND_PID > /dev/null 2>&1; then
        echo -e "${RED}⚠️  Frontend process died unexpectedly${NC}"
        echo -e "${YELLOW}Check frontend.log for errors${NC}"
        cleanup
    fi
done
