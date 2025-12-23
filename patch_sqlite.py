import sqlite3
import os

def patch_sqlite():
    db_path = "fastfoodie.db"
    if not os.path.exists(db_path):
        print(f"❌ Database file {db_path} not found.")
        return

    print(f"Patching database: {db_path}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check device_tokens table
    cursor.execute("PRAGMA table_info(device_tokens)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if "customer_id" not in columns:
        print("Adding customer_id to device_tokens...")
        try:
            cursor.execute("ALTER TABLE device_tokens ADD COLUMN customer_id INTEGER")
            print("✅ Added customer_id")
        except Exception as e:
            print(f"❌ Error adding customer_id: {e}")

    if "delivery_partner_id" not in columns:
        print("Adding delivery_partner_id to device_tokens...")
        try:
            cursor.execute("ALTER TABLE device_tokens ADD COLUMN delivery_partner_id INTEGER")
            print("✅ Added delivery_partner_id")
        except Exception as e:
            print(f"❌ Error adding delivery_partner_id: {e}")

    # Check orders table
    cursor.execute("PRAGMA table_info(orders)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if "released_at" not in columns:
        print("Adding released_at to orders...")
        try:
            cursor.execute("ALTER TABLE orders ADD COLUMN released_at DATETIME")
            print("✅ Added released_at")
        except Exception as e:
            print(f"❌ Error adding released_at: {e}")

    # Check notifications table (just in case)
    cursor.execute("PRAGMA table_info(notifications)")
    columns = [col[1] for col in cursor.fetchall()]
    
    for col_name in ["owner_id", "customer_id", "delivery_partner_id", "order_id"]:
        if col_name not in columns:
            print(f"Adding {col_name} to notifications...")
            try:
                cursor.execute(f"ALTER TABLE notifications ADD COLUMN {col_name} INTEGER")
                print(f"✅ Added {col_name}")
            except Exception as e:
                print(f"❌ Error adding {col_name}: {e}")

    conn.commit()
    conn.close()
    print("Done.")

if __name__ == "__main__":
    patch_sqlite()
