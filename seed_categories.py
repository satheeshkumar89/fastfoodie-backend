"""
Seed Categories Script

This script seeds the database with 60 predefined menu categories.
Run this after creating the categories table.

Usage:
    python seed_categories.py
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from app.database import SessionLocal
from app.models import Category
from datetime import datetime


CATEGORIES = [
    {"id": 1, "name": "Beverages", "display_order": 1},
    {"id": 2, "name": "Breakfast", "display_order": 2},
    {"id": 3, "name": "Biryani", "display_order": 3},
    {"id": 4, "name": "Burgers", "display_order": 4},
    {"id": 5, "name": "Chinese", "display_order": 5},
    {"id": 6, "name": "North Indian", "display_order": 6},
    {"id": 7, "name": "South Indian", "display_order": 7},
    {"id": 8, "name": "Pizzas", "display_order": 8},
    {"id": 9, "name": "Desserts", "display_order": 9},
    {"id": 10, "name": "Salads", "display_order": 10},
    {"id": 11, "name": "Snacks", "display_order": 11},
    {"id": 12, "name": "Seafood", "display_order": 12},
    {"id": 13, "name": "BBQ & Grill", "display_order": 13},
    {"id": 14, "name": "Healthy Food", "display_order": 14},
    {"id": 15, "name": "Combos & Meals", "display_order": 15},
    {"id": 16, "name": "Pure Veg", "display_order": 16},
    {"id": 17, "name": "Ice Creams", "display_order": 17},
    {"id": 18, "name": "Indian Breads", "display_order": 18},
    {"id": 19, "name": "Thali", "display_order": 19},
    {"id": 20, "name": "Rice Bowls", "display_order": 20},
    {"id": 21, "name": "Pasta", "display_order": 21},
    {"id": 22, "name": "Sandwiches", "display_order": 22},
    {"id": 23, "name": "Wraps & Rolls", "display_order": 23},
    {"id": 24, "name": "Shawarma", "display_order": 24},
    {"id": 25, "name": "Momos", "display_order": 25},
    {"id": 26, "name": "Fried Rice & Noodles", "display_order": 26},
    {"id": 27, "name": "Chaat", "display_order": 27},
    {"id": 28, "name": "Sweets", "display_order": 28},
    {"id": 29, "name": "Bakery", "display_order": 29},
    {"id": 30, "name": "Tandoori", "display_order": 30},
    {"id": 31, "name": "Kebabs", "display_order": 31},
    {"id": 32, "name": "Gravy Dishes", "display_order": 32},
    {"id": 33, "name": "Soups", "display_order": 33},
    {"id": 34, "name": "Starters", "display_order": 34},
    {"id": 35, "name": "Curries", "display_order": 35},
    {"id": 36, "name": "Juices", "display_order": 36},
    {"id": 37, "name": "Shakes", "display_order": 37},
    {"id": 38, "name": "Tea & Coffee", "display_order": 38},
    {"id": 39, "name": "Appetizers", "display_order": 39},
    {"id": 40, "name": "Gujarati", "display_order": 40},
    {"id": 41, "name": "Rajasthani", "display_order": 41},
    {"id": 42, "name": "Andhra", "display_order": 42},
    {"id": 43, "name": "Hyderabadi", "display_order": 43},
    {"id": 44, "name": "Punjabi", "display_order": 44},
    {"id": 45, "name": "Mughlai", "display_order": 45},
    {"id": 46, "name": "Arabian", "display_order": 46},
    {"id": 47, "name": "Thai", "display_order": 47},
    {"id": 48, "name": "Japanese", "display_order": 48},
    {"id": 49, "name": "Korean", "display_order": 49},
    {"id": 50, "name": "Italian", "display_order": 50},
    {"id": 51, "name": "Mexican", "display_order": 51},
    {"id": 52, "name": "American", "display_order": 52},
    {"id": 53, "name": "Mediterranean", "display_order": 53},
    {"id": 54, "name": "Street Food", "display_order": 54},
    {"id": 55, "name": "Organic", "display_order": 55},
    {"id": 56, "name": "Vegan", "display_order": 56},
    {"id": 57, "name": "Jain Friendly", "display_order": 57},
    {"id": 58, "name": "Kids Menu", "display_order": 58},
    {"id": 59, "name": "Party Packs", "display_order": 59},
    {"id": 60, "name": "Weekend Specials", "display_order": 60}
]


def seed_categories():
    """Seed the database with predefined categories"""
    db = SessionLocal()
    
    try:
        print("🌱 Starting category seeding...")
        
        # Check if categories already exist
        existing_count = db.query(Category).count()
        if existing_count > 0:
            print(f"⚠️  Found {existing_count} existing categories.")
            response = input("Do you want to clear and reseed? (yes/no): ")
            if response.lower() != 'yes':
                print("❌ Seeding cancelled.")
                return
            
            # Clear existing categories
            db.query(Category).delete()
            db.commit()
            print("🗑️  Cleared existing categories.")
        
        # Insert categories
        added_count = 0
        for cat_data in CATEGORIES:
            category = Category(
                id=cat_data['id'],
                name=cat_data['name'],
                icon=None,
                is_active=True,
                display_order=cat_data['display_order']
            )
            db.add(category)
            added_count += 1
        
        db.commit()
        print(f"✅ Successfully seeded {added_count} categories!")
        
        # Display categories
        print("\n📋 Categories added:")
        for cat in CATEGORIES[:10]:  # Show first 10
            print(f"   {cat['id']:2d}. {cat['name']}")
        print(f"   ... and {len(CATEGORIES) - 10} more")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding categories: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_categories()
