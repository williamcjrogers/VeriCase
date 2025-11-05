#!/usr/bin/env python3
"""Railway startup script with proper PORT handling"""
import os
import subprocess
import sys

# Get PORT from environment (Railway sets this automatically)
port = os.getenv('PORT', os.getenv('API_PORT', '8000'))

print(f"🔄 Running database migrations...")
migration_result = subprocess.run(['alembic', 'upgrade', 'head'], check=False)
if migration_result.returncode != 0:
    print("⚠️  Migration failed, continuing anyway...")

print(f"🚀 Starting Uvicorn on port {port}...")
print(f"📍 Environment: PORT={os.getenv('PORT')}, API_PORT={os.getenv('API_PORT')}")

# Start uvicorn
os.execvp('uvicorn', [
    'uvicorn',
    'app.main:app',
    '--host', '0.0.0.0',
    '--port', str(port)
])
