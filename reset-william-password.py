#!/usr/bin/env python3
import os
from passlib.hash import pbkdf2_sha256
from sqlalchemy import create_engine, text

# Hash the password "password"
password_hash = pbkdf2_sha256.hash("password")

# Update the database
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+psycopg2://vericase:vericase@localhost:55432/vericase')
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    result = conn.execute(
        text("UPDATE users SET password_hash = :hash WHERE email = :email"),
        {"hash": password_hash, "email": "william.rogers@quantumcommercialsolutions.com"}
    )
    conn.commit()
    print(f'✅ Reset password for william.rogers@quantumcommercialsolutions.com')
    print(f'   Email: william.rogers@quantumcommercialsolutions.com')
    print(f'   Password: password')
