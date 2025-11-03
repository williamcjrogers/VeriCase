import os
from sqlalchemy import create_engine, text

engine = create_engine(os.getenv('DATABASE_URL'))
with engine.connect() as conn:
    result = conn.execute(text("UPDATE users SET role = 'admin' WHERE email = 'william.rogers@quantumcommercialsolutions.com'"))
    conn.commit()
    print(f'✅ Updated {result.rowcount} user(s) to admin')
