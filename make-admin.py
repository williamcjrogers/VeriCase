#!/usr/bin/env python3
"""
Make william.rogers@quantumcommercialsolutions.com an admin
"""
import sys
import os

# Get DATABASE_URL from environment or command line
if len(sys.argv) > 1:
    DATABASE_URL = sys.argv[1]
else:
    DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    print("Usage: python make-admin.py <DATABASE_URL>")
    print("Or set DATABASE_URL environment variable")
    sys.exit(1)

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Create engine
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

try:
    # Update user role to admin
    result = session.execute(
        text("UPDATE users SET role = 'admin' WHERE email = 'william.rogers@quantumcommercialsolutions.com'")
    )
    session.commit()
    
    if result.rowcount > 0:
        print(f"✅ SUCCESS: william.rogers@quantumcommercialsolutions.com is now an admin!")
        print(f"   {result.rowcount} user(s) updated")
    else:
        print("❌ User not found. They need to sign up first.")
        print("\nTo create the admin user:")
        print("1. Sign up at the website with william.rogers@quantumcommercialsolutions.com")
        print("2. Then run this script again")
    
except Exception as e:
    print(f"❌ Error: {e}")
    session.rollback()
finally:
    session.close()
