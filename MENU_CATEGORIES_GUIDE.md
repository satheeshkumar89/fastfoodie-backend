# 🍽️ Menu Categories with IDs - Complete Guide

## 📋 Overview

The FastFoodie backend now uses a **proper Category system with IDs** instead of simple strings. This provides:
- ✅ Predefined list of 60 categories
- ✅ Consistent category naming across all restaurants
- ✅ Easy filtering and querying
- ✅ Better data integrity with foreign keys
- ✅ Ability to add icons and ordering

---

## 🗄️ Database Schema

### Categories Table
```sql
CREATE TABLE categories (
    id INT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    icon VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    display_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Menu Items Table (Updated)
```sql
ALTER TABLE menu_items 
ADD COLUMN category_id INT,
ADD FOREIGN KEY (category_id) REFERENCES categories(id);
```

---

## 📊 60 Predefined Categories

```json
{
  "success": true,
  "categories": [
    { "id": 1, "name": "Beverages" },
    { "id": 2, "name": "Breakfast" },
    { "id": 3, "name": "Biryani" },
    { "id": 4, "name": "Burgers" },
    { "id": 5, "name": "Chinese" },
    { "id": 6, "name": "North Indian" },
    { "id": 7, "name": "South Indian" },
    { "id": 8, "name": "Pizzas" },
    { "id": 9, "name": "Desserts" },
    { "id": 10, "name": "Salads" },
    { "id": 11, "name": "Snacks" },
    { "id": 12, "name": "Seafood" },
    { "id": 13, "name": "BBQ & Grill" },
    { "id": 14, "name": "Healthy Food" },
    { "id": 15, "name": "Combos & Meals" },
    { "id": 16, "name": "Pure Veg" },
    { "id": 17, "name": "Ice Creams" },
    { "id": 18, "name": "Indian Breads" },
    { "id": 19, "name": "Thali" },
    { "id": 20, "name": "Rice Bowls" },
    { "id": 21, "name": "Pasta" },
    { "id": 22, "name": "Sandwiches" },
    { "id": 23, "name": "Wraps & Rolls" },
    { "id": 24, "name": "Shawarma" },
    { "id": 25, "name": "Momos" },
    { "id": 26, "name": "Fried Rice & Noodles" },
    { "id": 27, "name": "Chaat" },
    { "id": 28, "name": "Sweets" },
    { "id": 29, "name": "Bakery" },
    { "id": 30, "name": "Tandoori" },
    { "id": 31, "name": "Kebabs" },
    { "id": 32, "name": "Gravy Dishes" },
    { "id": 33, "name": "Soups" },
    { "id": 34, "name": "Starters" },
    { "id": 35, "name": "Curries" },
    { "id": 36, "name": "Juices" },
    { "id": 37, "name": "Shakes" },
    { "id": 38, "name": "Tea & Coffee" },
    { "id": 39, "name": "Appetizers" },
    { "id": 40, "name": "Gujarati" },
    { "id": 41, "name": "Rajasthani" },
    { "id": 42, "name": "Andhra" },
    { "id": 43, "name": "Hyderabadi" },
    { "id": 44, "name": "Punjabi" },
    { "id": 45, "name": "Mughlai" },
    { "id": 46, "name": "Arabian" },
    { "id": 47, "name": "Thai" },
    { "id": 48, "name": "Japanese" },
    { "id": 49, "name": "Korean" },
    { "id": 50, "name": "Italian" },
    { "id": 51, "name": "Mexican" },
    { "id": 52, "name": "American" },
    { "id": 53, "name": "Mediterranean" },
    { "id": 54, "name": "Street Food" },
    { "id": 55, "name": "Organic" },
    { "id": 56, "name": "Vegan" },
    { "id": 57, "name": "Jain Friendly" },
    { "id": 58, "name": "Kids Menu" },
    { "id": 59, "name": "Party Packs" },
    { "id": 60, "name": "Weekend Specials" }
  ]
}
```

---

## 🚀 Setup Instructions

### Option 1: Using SQL Migration (Recommended)

```bash
# 1. Run the SQL migration
mysql -u your_user -p fastfoodie_db < migrations/add_categories.sql

# 2. Verify categories were added
mysql -u your_user -p fastfoodie_db -e "SELECT COUNT(*) FROM categories;"
```

### Option 2: Using Python Seed Script

```bash
# 1. Make sure your database is running
# 2. Run the seed script
python seed_categories.py
```

---

## 🎯 API Endpoints

### 1. Get All Categories

**Endpoint:** `GET /menu/categories`

**Authentication:** Not required (public endpoint)

**Response:**
```json
{
  "success": true,
  "message": "Menu categories retrieved successfully",
  "data": {
    "categories": [
      {
        "id": 1,
        "name": "Beverages",
        "icon": null,
        "is_active": true,
        "display_order": 1
      },
      {
        "id": 2,
        "name": "Breakfast",
        "icon": null,
        "is_active": true,
        "display_order": 2
      }
      // ... more categories
    ]
  }
}
```

**cURL Example:**
```bash
curl -X GET "http://localhost:8000/menu/categories"
```

---

### 2. Add Menu Item with Category

**Endpoint:** `POST /menu/item/add`

**Authentication:** Required (Bearer token)

**Request Body:**
```json
{
  "name": "Margherita Pizza",
  "description": "Classic pizza with tomato sauce and mozzarella",
  "price": 299.00,
  "discount_price": 249.00,
  "image_url": "https://example.com/margherita.jpg",
  "category_id": 8,  // ← Use category ID (8 = Pizzas)
  "is_vegetarian": true,
  "is_available": true,
  "preparation_time": 20
}
```

**Response:**
```json
{
  "success": true,
  "message": "Menu item added successfully",
  "data": {
    "id": 1,
    "name": "Margherita Pizza",
    "category_id": 8,
    "category": {
      "id": 8,
      "name": "Pizzas",
      "icon": null,
      "is_active": true,
      "display_order": 8
    },
    "price": 299.00,
    "is_vegetarian": true,
    ...
  }
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/menu/item/add" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Margherita Pizza",
    "price": 299.00,
    "category_id": 8,
    "is_vegetarian": true,
    "is_available": true
  }'
```

---

### 3. Get Menu Items by Category

**Endpoint:** `GET /menu/items?category_id={id}`

**Authentication:** Required (Bearer token)

**Example:** Get all Pizzas (category_id = 8)
```bash
curl -X GET "http://localhost:8000/menu/items?category_id=8" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**
```json
{
  "success": true,
  "message": "Menu items retrieved successfully",
  "data": {
    "items": [
      {
        "id": 1,
        "name": "Margherita Pizza",
        "category_id": 8,
        "category": {
          "id": 8,
          "name": "Pizzas"
        },
        "price": 299.00,
        ...
      },
      {
        "id": 2,
        "name": "Pepperoni Pizza",
        "category_id": 8,
        "category": {
          "id": 8,
          "name": "Pizzas"
        },
        "price": 349.00,
        ...
      }
    ]
  }
}
```

---

### 4. Update Menu Item Category

**Endpoint:** `PUT /menu/item/update/{item_id}`

**Request Body:**
```json
{
  "category_id": 10  // Change to Salads
}
```

---

## 📱 Flutter Implementation

### 1. Load Categories

```dart
class CategoryService {
  Future<List<Category>> loadCategories() async {
    final response = await api.get('/menu/categories');
    
    if (response['success']) {
      final categories = response['data']['categories'] as List;
      return categories.map((cat) => Category.fromJson(cat)).toList();
    }
    
    throw Exception('Failed to load categories');
  }
}
```

### 2. Category Model

```dart
class Category {
  final int id;
  final String name;
  final String? icon;
  final bool isActive;
  final int displayOrder;
  
  Category({
    required this.id,
    required this.name,
    this.icon,
    required this.isActive,
    required this.displayOrder,
  });
  
  factory Category.fromJson(Map<String, dynamic> json) {
    return Category(
      id: json['id'],
      name: json['name'],
      icon: json['icon'],
      isActive: json['is_active'],
      displayOrder: json['display_order'],
    );
  }
}
```

### 3. Display Categories as Tabs

```dart
class CategoryTabs extends StatelessWidget {
  final List<Category> categories;
  final int? selectedCategoryId;
  final Function(int) onCategorySelected;
  
  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 50,
      child: ListView.builder(
        scrollDirection: Axis.horizontal,
        itemCount: categories.length,
        itemBuilder: (context, index) {
          final category = categories[index];
          final isSelected = category.id == selectedCategoryId;
          
          return Padding(
            padding: EdgeInsets.symmetric(horizontal: 4),
            child: ChoiceChip(
              label: Text(category.name),
              selected: isSelected,
              onSelected: (_) => onCategorySelected(category.id),
              selectedColor: Colors.orange,
              backgroundColor: Colors.grey[200],
            ),
          );
        },
      ),
    );
  }
}
```

### 4. Add Menu Item with Category

```dart
Future<void> addMenuItem({
  required String name,
  required double price,
  required int categoryId,  // Use category ID
  bool isVegetarian = false,
}) async {
  final response = await api.post('/menu/item/add', {
    'name': name,
    'price': price,
    'category_id': categoryId,  // Send category_id
    'is_vegetarian': isVegetarian,
    'is_available': true,
  });
  
  if (response['success']) {
    print('Menu item added: ${response['data']}');
  }
}
```

---

## 🔄 Migration from Old System

If you have existing menu items with category strings:

### Automatic Migration
The SQL migration script automatically migrates existing category strings to IDs:

```sql
UPDATE menu_items m
JOIN categories c ON LOWER(m.category) = LOWER(c.name)
SET m.category_id = c.id
WHERE m.category IS NOT NULL;
```

### Manual Migration (if needed)
```python
# Python script to migrate
from app.database import SessionLocal
from app.models import MenuItem, Category

db = SessionLocal()

# Get all menu items with old category strings
items = db.query(MenuItem).filter(MenuItem.category.isnot(None)).all()

for item in items:
    # Find matching category
    category = db.query(Category).filter(
        Category.name.ilike(item.category)
    ).first()
    
    if category:
        item.category_id = category.id
        print(f"Migrated: {item.name} -> {category.name}")

db.commit()
```

---

## 🧪 Testing

### Test 1: Get All Categories
```bash
curl -X GET "http://localhost:8000/menu/categories"
```

**Expected:** 60 categories returned

### Test 2: Add Item with Category ID
```bash
curl -X POST "http://localhost:8000/menu/item/add" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Masala Dosa",
    "price": 120.00,
    "category_id": 7,
    "is_vegetarian": true,
    "is_available": true
  }'
```

**Expected:** Item created with category "South Indian"

### Test 3: Filter by Category
```bash
curl -X GET "http://localhost:8000/menu/items?category_id=7" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Expected:** Only South Indian items returned

### Test 4: Invalid Category ID
```bash
curl -X POST "http://localhost:8000/menu/item/add" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Item",
    "price": 100.00,
    "category_id": 999,
    "is_available": true
  }'
```

**Expected:** 404 error - "Category with id 999 not found"

---

## 💡 Best Practices

### 1. Always Use Category IDs
✅ **Good:**
```json
{
  "name": "Chicken Biryani",
  "category_id": 3
}
```

❌ **Bad (Old way):**
```json
{
  "name": "Chicken Biryani",
  "category": "Biryani"
}
```

### 2. Validate Category IDs in Frontend
```dart
// Load categories first
final categories = await loadCategories();

// Show dropdown with valid categories
DropdownButton<int>(
  items: categories.map((cat) => DropdownMenuItem(
    value: cat.id,
    child: Text(cat.name),
  )).toList(),
  onChanged: (categoryId) {
    // Use validated category ID
  },
);
```

### 3. Handle Null Categories
Items without categories are valid:
```json
{
  "name": "Special Item",
  "category_id": null,  // No category
  "price": 199.00
}
```

---

## ❓ FAQ

### Q: Can I add custom categories?
**A:** Currently, categories are predefined. If you need a new category, you'll need to add it to the database manually or request it to be added to the system.

### Q: What if I use an invalid category_id?
**A:** The API will return a 404 error: "Category with id X not found"

### Q: Can I filter by multiple categories?
**A:** Currently, the API supports filtering by one category at a time. For multiple categories, make separate requests or extend the API.

### Q: How do I get the category name from an item?
**A:** The MenuItemResponse includes the full category object:
```json
{
  "id": 1,
  "name": "Pizza",
  "category_id": 8,
  "category": {
    "id": 8,
    "name": "Pizzas"
  }
}
```

### Q: Can I deactivate a category?
**A:** Yes, update the `is_active` field in the database. Inactive categories won't appear in the GET /menu/categories response.

---

## ✅ Summary

### Changes Made:
1. ✅ Created `categories` table with 60 predefined categories
2. ✅ Updated `menu_items` table to use `category_id` foreign key
3. ✅ Updated API endpoints to work with category IDs
4. ✅ Added validation for category IDs
5. ✅ Included category object in menu item responses

### Migration Steps:
1. Run SQL migration: `migrations/add_categories.sql`
2. OR run Python seed: `python seed_categories.py`
3. Update your frontend to use `category_id` instead of `category` string
4. Test with Postman or cURL

### API Endpoints:
- `GET /menu/categories` - Get all categories
- `POST /menu/item/add` - Add item with `category_id`
- `GET /menu/items?category_id=X` - Filter by category
- `PUT /menu/item/update/{id}` - Update item category

**Your category system is ready!** 🎉
