#!/usr/bin/env python3
"""
Railway Database Fix Script
Migrates orphaned emails and assigns demo user to case
"""
import os
import psycopg2
from psycopg2.extras import RealDictCursor

def main():
    # Railway DATABASE_URL format: postgresql+psycopg2://user:pass@host:port/db
    db_url = os.getenv('DATABASE_URL', 'postgresql+psycopg2://vericase:vericase@postgres:5432/vericase')
    
    # Convert SQLAlchemy format to psycopg2 format
    db_url = db_url.replace('postgresql+psycopg2://', 'postgresql://')
    
    print(f"🔌 Connecting to Railway PostgreSQL...")
    conn = psycopg2.connect(db_url)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # Step 1: Check for orphaned emails
        print("\n📊 Checking for orphaned emails in null UUID case...")
        cursor.execute("""
            SELECT COUNT(*) as count 
            FROM evidence 
            WHERE case_id = '00000000-0000-0000-0000-000000000001'
        """)
        orphaned_count = cursor.fetchone()['count']
        print(f"   Found {orphaned_count} orphaned emails")
        
        # Step 2: Get most recent case
        print("\n🔍 Finding most recent case...")
        cursor.execute("SELECT id, name FROM cases ORDER BY created_at DESC LIMIT 1")
        target_case = cursor.fetchone()
        
        if not target_case:
            print("❌ ERROR: No cases found! Create a case first via wizard.")
            return
        
        print(f"   Target case: {target_case['id']} - {target_case['name']}")
        
        # Step 3: Migrate orphaned emails
        if orphaned_count > 0:
            print(f"\n🚚 Migrating {orphaned_count} emails to case {target_case['id']}...")
            cursor.execute("""
                UPDATE evidence 
                SET case_id = %s 
                WHERE case_id = '00000000-0000-0000-0000-000000000001'
            """, (target_case['id'],))
            conn.commit()
            print(f"   ✅ Migrated {cursor.rowcount} records")
        else:
            print("   ℹ️  No orphaned emails to migrate")
        
        # Step 4: Check for demo user
        print("\n👤 Checking for demo user...")
        cursor.execute("SELECT id, email FROM users WHERE email = 'demo@vericase.com'")
        demo_user = cursor.fetchone()
        
        if not demo_user:
            print("   ⚠️  Demo user not found - create via /api/auth/register")
        else:
            print(f"   Found demo user: {demo_user['id']}")
            
            # Step 5: Check if user already assigned to case
            cursor.execute("""
                SELECT id FROM case_users 
                WHERE user_id = %s AND case_id = %s
            """, (demo_user['id'], target_case['id']))
            
            if cursor.fetchone():
                print("   ℹ️  Demo user already assigned to case")
            else:
                # Step 6: Assign user to case
                print(f"\n🔗 Assigning demo user to case...")
                cursor.execute("""
                    INSERT INTO case_users (id, user_id, case_id, role, added_by_id)
                    VALUES (gen_random_uuid(), %s, %s, 'owner', %s)
                """, (demo_user['id'], target_case['id'], demo_user['id']))
                conn.commit()
                print("   ✅ User assigned as owner")
        
        # Step 7: Verify final state
        print("\n📈 Final email distribution:")
        cursor.execute("""
            SELECT c.id, c.name, COUNT(e.id) as email_count 
            FROM cases c 
            LEFT JOIN evidence e ON c.id = e.case_id AND e.email_from IS NOT NULL
            GROUP BY c.id 
            ORDER BY email_count DESC
            LIMIT 5
        """)
        
        for row in cursor.fetchall():
            print(f"   • {row['name']}: {row['email_count']} emails")
        
        print("\n✅ Railway database fixes complete!")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    main()
