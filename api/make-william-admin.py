#!/usr/bin/env python3
"""Make william.rogers@quantumcommercialsolutions.com an admin user"""
import os
import sys
from sqlalchemy import create_engine, text

def main():
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        print("❌ DATABASE_URL not set")
        sys.exit(1)
    
    engine = create_engine(db_url)
    
    with engine.connect() as conn:
        # Update the user to admin role
        result = conn.execute(text(
            "UPDATE users SET role = 'admin' WHERE email = 'william.rogers@quantumcommercialsolutions.com'"
        ))
        conn.commit()
        
        if result.rowcount > 0:
            print(f"✅ Updated {result.rowcount} user(s) to admin role")
        else:
            print("⚠️  No user found with email william.rogers@quantumcommercialsolutions.com")
            print("   Make sure the user has signed up first")

if __name__ == "__main__":
    main()
