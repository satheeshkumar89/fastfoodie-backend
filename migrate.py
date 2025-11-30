"""
Database initialization and migration script
This script creates all tables and seeds initial data
"""

from app.database import engine, Base, SessionLocal
from app.models import Cuisine, RestaurantTypeEnum
import sys


def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created successfully")


def seed_cuisines():
    """Seed initial cuisine data"""
    print("Seeding cuisine data...")
    
    cuisines = [
        {"name": "North Indian", "icon": "🍛"},
        {"name": "South Indian", "icon": "🥘"},
        {"name": "Chinese", "icon": "🥡"},
        {"name": "Italian", "icon": "🍝"},
        {"name": "Mexican", "icon": "🌮"},
        {"name": "Continental", "icon": "🍽️"},
        {"name": "Bakery", "icon": "🍰"},
        {"name": "Fast Food", "icon": "🍔"},
        {"name": "Street Food", "icon": "🌭"},
        {"name": "Desserts", "icon": "🍨"},
        {"name": "Beverages", "icon": "🥤"},
        {"name": "Healthy", "icon": "🥗"},
        {"name": "Seafood", "icon": "🦞"},
        {"name": "BBQ", "icon": "🍖"},
        {"name": "Pizza", "icon": "🍕"},
    ]
    
    db = SessionLocal()
    try:
        for cuisine_data in cuisines:
            # Check if cuisine already exists
            existing = db.query(Cuisine).filter(
                Cuisine.name == cuisine_data["name"]
            ).first()
            
            if not existing:
                cuisine = Cuisine(**cuisine_data)
                db.add(cuisine)
        
        db.commit()
        print(f"✓ Seeded {len(cuisines)} cuisines")
    except Exception as e:
        print(f"✗ Error seeding cuisines: {e}")
        db.rollback()
    finally:
        db.close()


def main():
    """Main migration function"""
    print("=" * 50)
    print("FastFoodie Database Migration")
    print("=" * 50)
    
    try:
        create_tables()
        seed_cuisines()
        
        print("\n" + "=" * 50)
        print("✓ Migration completed successfully!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n✗ Migration failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
