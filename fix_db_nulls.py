import sqlite3
import os

def fix_device_tokens_nullability():
    db_path = "fastfoodie.db"
    if not os.path.exists(db_path):
        print(f"❌ Database file {db_path} not found.")
        return

    print(f"Fixing nullability for device_tokens in {db_path}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # 1. Rename old table
        cursor.execute("ALTER TABLE device_tokens RENAME TO device_tokens_old")
        
        # 2. Create new table with correct schema (nullable owner_id)
        # We also need to include the columns we added earlier
        cursor.execute("""
            CREATE TABLE device_tokens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                owner_id INTEGER NULL,
                customer_id INTEGER NULL,
                delivery_partner_id INTEGER NULL,
                token VARCHAR(500) UNIQUE NOT NULL,
                device_type VARCHAR(50) NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME,
                FOREIGN KEY (owner_id) REFERENCES owners (id),
                FOREIGN KEY (customer_id) REFERENCES customers (id),
                FOREIGN KEY (delivery_partner_id) REFERENCES delivery_partners (id)
            )
        """)
        
        # 3. Copy data from old table
        # We need to map the columns correctly
        cursor.execute("PRAGMA table_info(device_tokens_old)")
        old_columns = [col[1] for col in cursor.fetchall()]
        
        common_columns = ["id", "owner_id", "token", "device_type", "is_active", "created_at", "updated_at"]
        # Only copy columns that existed in the old table
        cols_to_copy = [c for c in common_columns if c in old_columns]
        
        # Also check for customer_id if it was already added by the previous patch
        if "customer_id" in old_columns:
            cols_to_copy.append("customer_id")
        if "delivery_partner_id" in old_columns:
            cols_to_copy.append("delivery_partner_id")
            
        cols_str = ", ".join(cols_to_copy)
        cursor.execute(f"INSERT INTO device_tokens ({cols_str}) SELECT {cols_str} FROM device_tokens_old")
        
        # 4. Drop old table
        cursor.execute("DROP TABLE device_tokens_old")
        
        conn.commit()
        print("✅ Successfully recreated device_tokens table with correct nullability.")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error fixing nullability: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    fix_device_tokens_nullability()
