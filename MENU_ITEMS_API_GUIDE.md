# 📱 Menu Items API - Two Response Formats

## Overview

The FastFoodie backend now provides **TWO endpoints** for getting menu items:

1. **`GET /menu/items`** - Flat list (original)
2. **`GET /menu/items/grouped`** - Grouped by categories (for UI) ✨ **NEW!**

---

## 🎯 Endpoint 1: Flat List

### **`GET /menu/items`**

Returns a simple flat list of all menu items.

**Use Case:** When you need all items or filter by a specific category

**Request:**
```bash
GET /menu/items
GET /menu/items?category_id=8  # Filter by category
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
        "price": "299.00",
        "category_id": 8,
        "category": {
          "id": 8,
          "name": "Pizzas"
        }
      },
      {
        "id": 2,
        "name": "Chocolate Cake",
        "price": "6.99",
        "category_id": 9,
        "category": {
          "id": 9,
          "name": "Desserts"
        }
      }
    ]
  }
}
```

---

## 🎨 Endpoint 2: Grouped by Categories ✨ **NEW!**

### **`GET /menu/items/grouped`**

Returns items **grouped by their categories** - perfect for UI display!

**Use Case:** Menu Management screen with expandable category sections

**Request:**
```bash
GET /menu/items/grouped
```

**Response:**
```json
{
  "success": true,
  "message": "Menu items grouped by categories retrieved successfully",
  "data": {
    "categories": [
      {
        "category": {
          "id": 9,
          "name": "Desserts",
          "icon": null,
          "is_active": true,
          "display_order": 9
        },
        "items": [
          {
            "id": 4,
            "name": "Chocolate Cake",
            "description": "Rich chocolate cake with ganache",
            "price": "6.99",
            "discount_price": "0.00",
            "image_url": null,
            "category_id": 9,
            "category": {
              "id": 9,
              "name": "Desserts"
            },
            "is_vegetarian": true,
            "is_available": true,
            "preparation_time": 5,
            "created_at": "2025-11-26T06:18:58"
          },
          {
            "id": 5,
            "name": "Tiramisu",
            "price": "7.99",
            "category_id": 9,
            "is_vegetarian": true,
            "preparation_time": 5
          }
        ],
        "item_count": 2
      },
      {
        "category": {
          "id": 8,
          "name": "Pizzas",
          "display_order": 8
        },
        "items": [
          {
            "id": 2,
            "name": "Margherita Pizza",
            "price": "299.00",
            "discount_price": "249.00",
            "category_id": 8,
            "preparation_time": 20
          },
          {
            "id": 6,
            "name": "Pepperoni Pizza",
            "price": "14.99",
            "category_id": 8,
            "preparation_time": 22
          }
        ],
        "item_count": 2
      }
    ],
    "total_categories": 2,
    "total_items": 4
  }
}
```

---

## 📊 Response Structure Comparison

### Flat List (`/menu/items`):
```
{
  "data": {
    "items": [item1, item2, item3, ...]
  }
}
```

### Grouped (`/menu/items/grouped`):
```
{
  "data": {
    "categories": [
      {
        "category": {...},
        "items": [item1, item2],
        "item_count": 2
      },
      {
        "category": {...},
        "items": [item3, item4],
        "item_count": 2
      }
    ],
    "total_categories": 2,
    "total_items": 4
  }
}
```

---

## 📱 Flutter Implementation

### Using Grouped Endpoint (Recommended for UI)

```dart
// Model for grouped response
class CategoryWithItems {
  final Category? category;
  final List<MenuItem> items;
  final int itemCount;
  
  CategoryWithItems({
    this.category,
    required this.items,
    required this.itemCount,
  });
  
  factory CategoryWithItems.fromJson(Map<String, dynamic> json) {
    return CategoryWithItems(
      category: json['category'] != null 
          ? Category.fromJson(json['category']) 
          : null,
      items: (json['items'] as List)
          .map((item) => MenuItem.fromJson(item))
          .toList(),
      itemCount: json['item_count'],
    );
  }
}

// Load grouped items
Future<List<CategoryWithItems>> loadGroupedMenuItems() async {
  final response = await http.get(
    Uri.parse('http://localhost:8000/menu/items/grouped'),
    headers: {'Authorization': 'Bearer $token'},
  );
  
  if (response.statusCode == 200) {
    final data = json.decode(response.body);
    final categories = data['data']['categories'] as List;
    
    return categories
        .map((cat) => CategoryWithItems.fromJson(cat))
        .toList();
  }
  
  throw Exception('Failed to load menu items');
}

// Display in UI
class MenuManagementScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<CategoryWithItems>>(
      future: loadGroupedMenuItems(),
      builder: (context, snapshot) {
        if (!snapshot.hasData) return CircularProgressIndicator();
        
        final categoriesWithItems = snapshot.data!;
        
        return ListView.builder(
          itemCount: categoriesWithItems.length,
          itemBuilder: (context, index) {
            final categoryGroup = categoriesWithItems[index];
            
            return ExpansionTile(
              title: Text(
                categoryGroup.category?.name ?? 'Uncategorized',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
              subtitle: Text('${categoryGroup.itemCount} items'),
              children: categoryGroup.items.map((item) {
                return ListTile(
                  leading: item.imageUrl != null
                      ? Image.network(item.imageUrl!)
                      : Icon(Icons.fastfood),
                  title: Text(item.name),
                  subtitle: Text('\$${item.price}'),
                  trailing: Switch(
                    value: item.isAvailable,
                    onChanged: (value) => toggleAvailability(item.id, value),
                  ),
                );
              }).toList(),
            );
          },
        );
      },
    );
  }
}
```

---

## 🧪 Testing

### Test Grouped Endpoint
```bash
TOKEN="your_token_here"

curl -X GET "http://localhost:8000/menu/items/grouped" \
  -H "Authorization: Bearer $TOKEN" \
  | python -m json.tool
```

### Expected Output:
```json
{
  "success": true,
  "data": {
    "categories": [
      {
        "category": {"id": 9, "name": "Desserts"},
        "items": [...],
        "item_count": 2
      },
      {
        "category": {"id": 8, "name": "Pizzas"},
        "items": [...],
        "item_count": 2
      }
    ],
    "total_categories": 2,
    "total_items": 4
  }
}
```

---

## 💡 When to Use Which Endpoint?

### Use **`/menu/items`** when:
- ✅ You need a simple list of all items
- ✅ You want to filter by a specific category
- ✅ You're building a simple list view
- ✅ You need to search/filter items

### Use **`/menu/items/grouped`** when:
- ✅ You're building a menu management UI (like your screenshot)
- ✅ You want to display items organized by categories
- ✅ You need expandable category sections
- ✅ You want to show item counts per category
- ✅ You're building a categorized menu display

---

## ✅ Summary

| Feature | `/menu/items` | `/menu/items/grouped` |
|---------|---------------|----------------------|
| **Response Format** | Flat list | Grouped by categories |
| **Filtering** | ✅ By category_id | ❌ Returns all |
| **Category Info** | In each item | Separate category object |
| **Item Count** | ❌ No | ✅ Per category |
| **Best For** | Simple lists, filtering | UI with category sections |
| **UI Match** | List view | Your screenshot! |

---

## 🎯 Perfect Match for Your UI!

Your UI shows:
```
Desserts (2 items)
  - Chocolate Cake ($6.99)
  - Tiramisu ($7.99)

Pizzas (2 items)
  - Margherita Pizza ($12.99)
  - Pepperoni Pizza ($14.99)
```

Use **`GET /menu/items/grouped`** to get exactly this structure! ✨

---

**Both endpoints are now available and working!** 🚀
