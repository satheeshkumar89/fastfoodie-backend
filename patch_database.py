from sqlalchemy import create_engine, text
import os
import sys

# Get database URL from environment variable or use default
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://fastfoodie_user:fastfoodie_pass@localhost:3306/fastfoodie")

def patch_database():
    print(f"Connecting to database: {DATABASE_URL}")
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as connection:
            # 1. Patch otps table
            print("Checking otps table...")
            try:
                result = connection.execute(text("SHOW COLUMNS FROM otps LIKE 'customer_id'"))
                if not result.fetchone():
                    print("⚠️ Column 'customer_id' missing in 'otps'. Adding it...")
                    connection.execute(text("ALTER TABLE otps ADD COLUMN customer_id INT NULL"))
                    connection.execute(text("ALTER TABLE otps ADD CONSTRAINT fk_otps_customer_id FOREIGN KEY (customer_id) REFERENCES customers(id)"))
                    connection.commit()
            except Exception as e:
                print(f"❌ Error patching otps: {e}")

            # 2. Patch orders table
            print("Checking orders table...")
            try:
                result = connection.execute(text("SHOW COLUMNS FROM orders LIKE 'released_at'"))
                if not result.fetchone():
                    print("⚠️ Column 'released_at' missing in 'orders'. Adding it...")
                    connection.execute(text("ALTER TABLE orders ADD COLUMN released_at DATETIME NULL"))
                    connection.commit()
                    print("✅ Successfully added 'released_at' to 'orders'.")
                else:
                    print("✅ Column 'released_at' already exists in 'orders'.")
            except Exception as e:
                print(f"❌ Error patching orders: {e}")

            # 3. Patch device_tokens table
            print("Checking device_tokens table...")
            try:
                # Add customer_id
                result = connection.execute(text("SHOW COLUMNS FROM device_tokens LIKE 'customer_id'"))
                if not result.fetchone():
                    print("⚠️ Column 'customer_id' missing in 'device_tokens'. Adding it...")
                    connection.execute(text("ALTER TABLE device_tokens ADD COLUMN customer_id INT NULL"))
                    connection.execute(text("ALTER TABLE device_tokens ADD CONSTRAINT fk_dt_customer_id FOREIGN KEY (customer_id) REFERENCES customers(id)"))
                
                # Add delivery_partner_id
                result = connection.execute(text("SHOW COLUMNS FROM device_tokens LIKE 'delivery_partner_id'"))
                if not result.fetchone():
                    print("⚠️ Column 'delivery_partner_id' missing in 'device_tokens'. Adding it...")
                    connection.execute(text("ALTER TABLE device_tokens ADD COLUMN delivery_partner_id INT NULL"))
                    connection.execute(text("ALTER TABLE device_tokens ADD CONSTRAINT fk_dt_dp_id FOREIGN KEY (delivery_partner_id) REFERENCES delivery_partners(id)"))
                
                # Make owner_id nullable
                print("Ensuring owner_id is nullable in device_tokens...")
                connection.execute(text("ALTER TABLE device_tokens MODIFY COLUMN owner_id INT NULL"))
                
                connection.commit()
                print("✅ Successfully patched 'device_tokens'.")
            except Exception as e:
                print(f"❌ Error patching device_tokens: {e}")

            # 4. Create notifications table if not exists
            print("Checking notifications table...")
            try:
                connection.execute(text("""
                    CREATE TABLE IF NOT EXISTS notifications (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        owner_id INT NULL,
                        customer_id INT NULL,
                        delivery_partner_id INT NULL,
                        title VARCHAR(255) NOT NULL,
                        message TEXT NOT NULL,
                        notification_type VARCHAR(50),
                        order_id INT NULL,
                        is_read BOOLEAN DEFAULT FALSE,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (owner_id) REFERENCES owners(id),
                        FOREIGN KEY (customer_id) REFERENCES customers(id),
                        FOREIGN KEY (delivery_partner_id) REFERENCES delivery_partners(id),
                        FOREIGN KEY (order_id) REFERENCES orders(id)
                    )
                """))
                connection.commit()
                print("✅ Notifications table checked/created.")
            except Exception as e:
                print(f"❌ Error creating notifications table: {e}")
                
    except Exception as e:
        print(f"❌ Failed to connect to database: {e}")

if __name__ == "__main__":
    patch_database()
