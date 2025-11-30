# 🚀 Quick Start: Adding Categories to FastFoodie

## What Changed?

Categories now use **IDs instead of strings** with 60 predefined categories.

---

## 📋 Quick Setup (Choose One)

### Option 1: SQL Migration (Fastest)
```bash
# Run this SQL file
mysql -u root -p fastfoodie_db < migrations/add_categories.sql
```

### Option 2: Python Seed Script
```bash
# Run this Python script
python seed_categories.py
```

---

## 🎯 How to Use

### 1. Get All Categories
```bash
GET /menu/categories
```

**Response:**
```json
{
  "success": true,
  "categories": [
    { "id": 1, "name": "Beverages" },
    { "id": 8, "name": "Pizzas" },
    { "id": 3, "name": "Biryani" },
    ...
  ]
}
```

### 2. Add Menu Item with Category
```bash
POST /menu/item/add
```

**Before (Old):**
```json
{
  "name": "Margherita Pizza",
  "category": "Pizza",  ❌ String
  "price": 299.00
}
```

**Now (New):**
```json
{
  "name": "Margherita Pizza",
  "category_id": 8,  ✅ ID (8 = Pizzas)
  "price": 299.00
}
```

### 3. Filter by Category
```bash
GET /menu/items?category_id=8
```

---

## 📊 All 60 Categories

| ID | Category Name | ID | Category Name |
|----|--------------|----|--------------| 
| 1 | Beverages | 31 | Kebabs |
| 2 | Breakfast | 32 | Gravy Dishes |
| 3 | Biryani | 33 | Soups |
| 4 | Burgers | 34 | Starters |
| 5 | Chinese | 35 | Curries |
| 6 | North Indian | 36 | Juices |
| 7 | South Indian | 37 | Shakes |
| 8 | Pizzas | 38 | Tea & Coffee |
| 9 | Desserts | 39 | Appetizers |
| 10 | Salads | 40 | Gujarati |
| 11 | Snacks | 41 | Rajasthani |
| 12 | Seafood | 42 | Andhra |
| 13 | BBQ & Grill | 43 | Hyderabadi |
| 14 | Healthy Food | 44 | Punjabi |
| 15 | Combos & Meals | 45 | Mughlai |
| 16 | Pure Veg | 46 | Arabian |
| 17 | Ice Creams | 47 | Thai |
| 18 | Indian Breads | 48 | Japanese |
| 19 | Thali | 49 | Korean |
| 20 | Rice Bowls | 50 | Italian |
| 21 | Pasta | 51 | Mexican |
| 22 | Sandwiches | 52 | American |
| 23 | Wraps & Rolls | 53 | Mediterranean |
| 24 | Shawarma | 54 | Street Food |
| 25 | Momos | 55 | Organic |
| 26 | Fried Rice & Noodles | 56 | Vegan |
| 27 | Chaat | 57 | Jain Friendly |
| 28 | Sweets | 58 | Kids Menu |
| 29 | Bakery | 59 | Party Packs |
| 30 | Tandoori | 60 | Weekend Specials |

---

## 🔧 Files Modified

1. ✅ `app/models.py` - Added Category model, updated MenuItem
2. ✅ `app/schemas.py` - Added CategoryResponse, updated MenuItem schemas
3. ✅ `app/routers/menu.py` - Updated to use category_id
4. ✅ `migrations/add_categories.sql` - SQL migration script
5. ✅ `seed_categories.py` - Python seed script

---

## 📖 Full Documentation

See **MENU_CATEGORIES_GUIDE.md** for complete details!

---

**Ready to use!** 🎉
