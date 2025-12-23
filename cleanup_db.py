import sqlite3
import os

def clear_database():
    db_path = "fastfoodie.db"
    if not os.path.exists(db_path):
        print(f"❌ Database file {db_path} not found.")
        return

    print(f"🧹 Clearing all data from {db_path}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # List of tables to clear in order of dependency
    tables = [
        "order_items",
        "orders",
        "cart_items",
        "carts",
        "notifications",
        "device_tokens",
        "otps",
        "restaurant_cuisines",
        "documents",
        "customer_addresses",
        "reviews",
        "menu_items",
        "restaurants",
        "owners",
        "customers"
    ]

    try:
        # Disable foreign keys for bulk deletion
        cursor.execute("PRAGMA foreign_keys = OFF")
        
        for table in tables:
            try:
                cursor.execute(f"DELETE FROM {table}")
                print(f"✅ Cleared table: {table}")
            except Exception as e:
                # Table might not exist yet if migrations haven't run
                print(f"ℹ️ Skipping {table}: {e}")

        # Reset SQLite auto-increment counters
        cursor.execute("DELETE FROM sqlite_sequence")
        
        conn.commit()
        print("\n✨ All mobile numbers, users, and restaurants have been removed.")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error clearing data: {e}")
    finally:
        cursor.execute("PRAGMA foreign_keys = ON")
        conn.close()

if __name__ == "__main__":
    clear_database()
