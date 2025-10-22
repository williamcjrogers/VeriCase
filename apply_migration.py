#!/usr/bin/env python3
from app.db import engine

sql = """
-- Create user role enum
CREATE TYPE user_role AS ENUM ('admin', 'editor', 'viewer');

-- Add role and management columns to users table
ALTER TABLE users 
    ADD COLUMN IF NOT EXISTS role user_role DEFAULT 'editor',
    ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT true,
    ADD COLUMN IF NOT EXISTS last_login_at TIMESTAMP,
    ADD COLUMN IF NOT EXISTS display_name VARCHAR(255);
"""

with engine.begin() as conn:
    conn.execute(sql)
    
print("✅ Migration applied successfully! You can now log in.")
