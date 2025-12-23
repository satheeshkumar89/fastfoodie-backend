from sqlalchemy import create_engine, text
import os
import sys

# Get database URL from environment variable or use default
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Try reading from .env file directly
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            for line in f:
                if line.startswith("DATABASE_URL="):
                    DATABASE_URL = line.split("=", 1)[1].strip()
                    if DATABASE_URL.startswith('"') and DATABASE_URL.endswith('"'):
                        DATABASE_URL = DATABASE_URL[1:-1]
                    if DATABASE_URL.startswith("'") and DATABASE_URL.endswith("'"):
                        DATABASE_URL = DATABASE_URL[1:-1]
                    break

if not DATABASE_URL:
    print("❌ DATABASE_URL not found in environment or .env file.")
    sys.exit(1)

def clear_mysql_database():
    print(f"🧹 Connecting to MySQL to clear tables: {DATABASE_URL}")
    try:
        engine = create_engine(DATABASE_URL)
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
        
        with engine.connect() as connection:
            print("Disabling foreign key checks...")
            connection.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
            
            for table in tables:
                try:
                    connection.execute(text(f"TRUNCATE TABLE {table}"))
                    print(f"✅ Cleared table: {table}")
                except Exception as e:
                    print(f"ℹ️ Skipping {table} (not found or error): {e}")
            
            connection.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
            # Commit is handled automatically or by context in some engine setups, 
            # but MySQL TRUNCATE is an implicit commit.
            
            print("\n✨ All mobile numbers, users, and restaurants have been removed from MySQL.")

    except Exception as e:
        print(f"❌ Failed to clear database: {e}")

if __name__ == "__main__":
    confirm = input("ARE YOU SURE? This will delete ALL owners, customers, and restaurants. (y/n): ")
    if confirm.lower() == 'y':
        clear_mysql_database()
    else:
        print("Operation cancelled.")
