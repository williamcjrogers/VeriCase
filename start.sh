#!/bin/sh
set -e

echo "🔄 Running database migrations..."
alembic upgrade head

# Use Railway's API_PORT or fallback to Railway's $PORT or 8000
PORT="${PORT:-${API_PORT:-8000}}"

echo "🚀 Starting Uvicorn on port ${PORT}..."
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT}"
