from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://fastfoodie_user:fastfoodie_pass@localhost:3306/fastfoodie")
engine = create_engine(DATABASE_URL)

def activate_all():
    with engine.connect() as conn:
        print("Activating all owners...")
        conn.execute(text("UPDATE owners SET is_active = 1;"))
        print("Activating all customers...")
        conn.execute(text("UPDATE customers SET is_active = 1;"))
        conn.commit()
    print("Done!")

if __name__ == "__main__":
    activate_all()
