#!/bin/bash

# Exit if any command fails
set -e

# Project root
PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"

# Load environment variables from .env
if [ -f "$PROJECT_ROOT/.env" ]; then
  export $(grep -v '^#' "$PROJECT_ROOT/.env" | xargs)
fi

# Log files
LOG_DIR="$PROJECT_ROOT/logs"
mkdir -p "$LOG_DIR"
BOT_LOG="$LOG_DIR/bot.log"
BACKEND_LOG="$LOG_DIR/backend.log"

# Number of restart attempts
MAX_RETRIES=5
RETRY_DELAY=3

# Start Flask backend using Gunicorn
start_backend() {
  echo "🚀 Starting Flask backend..."
  cd "$PROJECT_ROOT/backend"
  gunicorn -w 4 app:app --bind 0.0.0.0:5000 >> "$BACKEND_LOG" 2>&1 &
  BACKEND_PID=$!
  echo "✅ Flask started [PID $BACKEND_PID]"
  cd "$PROJECT_ROOT"
}

# Start Telegram bot
start_bot() {
  echo "🤖 Starting Telegram bot..."
  cd "$PROJECT_ROOT/bot"
  python bot.py >> "$BOT_LOG" 2>&1 &
  BOT_PID=$!
  echo "✅ Bot started [PID $BOT_PID]"
  cd "$PROJECT_ROOT"
}

# Restart loop for processes
monitor_process() {
  local name=$1
  local start_cmd=$2
  local pid_var=$3
  local retries=0

  while true; do
    pid=${!pid_var}
    if ! kill -0 "$pid" 2>/dev/null; then
      echo "❌ $name crashed!"
      ((retries++))
      if [ "$retries" -gt "$MAX_RETRIES" ]; then
        echo "💥 $name exceeded max retries. Exiting..."
        kill $BACKEND_PID $BOT_PID 2>/dev/null || true
        exit 1
      fi
      echo "🔁 Restarting $name in $RETRY_DELAY seconds... (attempt $retries)"
      sleep "$RETRY_DELAY"
      eval "$start_cmd"
    fi
    sleep 5
  done
}

# Trap SIGINT and SIGTERM
cleanup() {
  echo "🛑 Shutting down..."
  kill $BACKEND_PID $BOT_PID 2>/dev/null || true
  exit 0
}
trap cleanup SIGINT SIGTERM

# Start both services
start_backend
start_bot

# Monitor both in background
monitor_process "Flask Backend" "start_backend" BACKEND_PID &
monitor_process "Telegram Bot" "start_bot" BOT_PID &

# Keep script running
wait
