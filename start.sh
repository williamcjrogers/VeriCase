#!/bin/sh
set -e

echo "🔄 Running database migrations..."
alembic upgrade head

# Railway provides PORT automatically, but fallback to API_PORT if not set
if [ -z "$PORT" ]; then
    PORT="${API_PORT:-8000}"
fi

echo "🚀 Starting Uvicorn on port ${PORT}..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT}
