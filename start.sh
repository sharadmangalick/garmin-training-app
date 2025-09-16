#!/bin/bash

# Garmin Training App Startup Script

echo "🏃‍♂️ Starting Garmin Training Dashboard..."
echo "========================================"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp env.example .env
    echo "📝 Please edit .env file with your Garmin Connect credentials"
    echo "   Then run this script again."
    exit 1
fi

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
fi

# Check if client/node_modules exists
if [ ! -d "client/node_modules" ]; then
    echo "📦 Installing React dependencies..."
    cd client && npm install && cd ..
fi

echo "🚀 Starting development servers..."
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Start both servers
npm run dev
