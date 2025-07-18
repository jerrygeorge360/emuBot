#!/bin/bash

# Exit if any command fails
set -e

# Set project root
PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_ROOT"

# Create log directory
mkdir -p logs

# Start backend
echo "🚀 Starting backend..."
python -m backend.app >> logs/backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend running in background [PID $BACKEND_PID]"

# Start bot
echo "Starting bot..."
python -m bot.bot >> logs/bot.log 2>&1 &
BOT_PID=$!
echo "✅ Bot running in background [PID $BOT_PID]"

# Wait to keep script running if desired
# wait $BACKEND_PID $BOT_PID
