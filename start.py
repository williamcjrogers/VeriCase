#!/usr/bin/env python3
"""Railway startup script - uses Railway's auto-injected PORT"""
import os
import subprocess
import sys

print("🔄 Running database migrations...")
migration_result = subprocess.run(['alembic', 'upgrade', 'head'], check=False)
if migration_result.returncode != 0:
    print("⚠️  Migration failed, continuing anyway...")

# Railway automatically injects PORT environment variable
# If not present, use API_PORT or default 8010
port = int(os.environ.get('PORT', os.environ.get('API_PORT', '8010')))

print(f"🚀 Starting Uvicorn on port {port}...")
print(f"📍 PORT={port} (from env: PORT={os.getenv('PORT')}, API_PORT={os.getenv('API_PORT')})")

# Start uvicorn with integer port
os.execvp('uvicorn', [
    'uvicorn',
    'app.main:app',
    '--host', '0.0.0.0',
    '--port', str(port)
])
