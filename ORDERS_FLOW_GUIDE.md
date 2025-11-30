# 🍽️ FastFoodie Orders Flow - Complete Guide

## ✅ Orders Successfully Created!

**28 realistic orders** have been seeded into your database:
- **5 NEW orders** - Waiting for restaurant acceptance
- **8 ONGOING orders** - In various stages (accepted, preparing, ready, picked up)
- **15 COMPLETED orders** - Delivered or rejected

---

## 📋 Order Endpoints

### 1. **GET /orders/new** - New Orders (Pending Acceptance)

Get all orders with status: `NEW`

**Request:**
```bash
GET /orders/new
Authorization: Bearer {token}
```

**Response:**
```json
{
  "success": true,
  "message": "New orders retrieved successfully",
  "data": {
    "orders": [
      {
        "order_id": 3,
        "item_count": 4,
        "total_amount": "471.55",
        "created_at": "2025-11-26T15:59:24.755455",
        "payment_method": "online",
        "status": "new"
      },
      {
        "order_id": 1,
        "item_count": 4,
        "total_amount": "399.10",
        "created_at": "2025-11-26T15:54:24.746727",
        "payment_method": "online",
        "status": "new"
      }
    ]
  }
}
```

---

### 2. **GET /orders/ongoing** - Ongoing Orders

Get all orders with status: `ACCEPTED`, `PREPARING`, `READY`, `PICKED_UP`

**Request:**
```bash
GET /orders/ongoing
Authorization: Bearer {token}
```

**Response:**
```json
{
  "success": true,
  "message": "Ongoing orders retrieved successfully",
  "data": {
    "orders": [
      {
        "order_id": 5,
        "item_count": 3,
        "total_amount": "273.10",
        "created_at": "2025-11-26T15:42:24.761267",
        "payment_method": "online",
        "status": "preparing"
      },
      {
        "order_id": 4,
        "item_count": 4,
        "total_amount": "399.10",
        "created_at": "2025-11-26T15:40:24.756544",
        "payment_method": "online",
        "status": "accepted"
      },
      {
        "order_id": 6,
        "item_count": 2,
        "total_amount": "219.55",
        "created_at": "2025-11-26T15:23:24.762486",
        "payment_method": "online",
        "status": "ready"
      }
    ]
  }
}
```

---

### 3. **GET /orders/completed** - Completed Orders

Get all orders with status: `DELIVERED`, `REJECTED`, `CANCELLED`

**Request:**
```bash
GET /orders/completed
Authorization: Bearer {token}
```

**Response:**
```json
{
  "success": true,
  "message": "Completed orders retrieved successfully",
  "data": {
    "orders": [
      {
        "order_id": 12,
        "item_count": 2,
        "total_amount": "219.55",
        "created_at": "2025-11-26T14:00:24.768022",
        "payment_method": "online",
        "status": "rejected"
      },
      {
        "order_id": 8,
        "item_count": 3,
        "total_amount": "345.55",
        "created_at": "2025-11-26T13:00:24.764152",
        "payment_method": "online",
        "status": "delivered"
      }
    ]
  }
}
```

---

### 4. **GET /orders/details/{order_id}** - Order Details

Get full details of a specific order including items, customer info, etc.

**Request:**
```bash
GET /orders/details/1
Authorization: Bearer {token}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "order_id": 1,
    "order_number": "ORD20251126155424",
    "customer_name": "Rajesh Kumar",
    "customer_phone": "+919876543210",
    "delivery_address": "123 MG Road, Bangalore, Karnataka 560001",
    "status": "new",
    "total_amount": "399.10",
    "delivery_fee": "30.00",
    "tax_amount": "17.10",
    "discount_amount": "0.00",
    "payment_method": "upi",
    "payment_status": "pending",
    "special_instructions": "Extra spicy please",
    "items": [
      {
        "menu_item_id": 2,
        "name": "Margherita Pizza",
        "quantity": 2,
        "price": "299.00",
        "special_instructions": null
      },
      {
        "menu_item_id": 4,
        "name": "Chocolate Cake",
        "quantity": 1,
        "price": "6.99",
        "special_instructions": "Extra chocolate"
      }
    ],
    "created_at": "2025-11-26T15:54:24",
    "estimated_delivery_time": "2025-11-26T16:24:24"
  }
}
```

---

## 🔄 Order Status Flow

### Order Lifecycle:

```
NEW → ACCEPTED → PREPARING → READY → PICKED_UP → DELIVERED
  ↓
REJECTED
```

### Status Update Endpoints:

#### 1. **Accept Order**
```bash
PUT /orders/accept/{order_id}
Authorization: Bearer {token}
```

#### 2. **Start Preparing**
```bash
PUT /orders/preparing/{order_id}
Authorization: Bearer {token}
```

#### 3. **Mark as Ready**
```bash
PUT /orders/ready/{order_id}
Authorization: Bearer {token}
```

#### 4. **Mark as Picked Up**
```bash
PUT /orders/pickedup/{order_id}
Authorization: Bearer {token}
```

#### 5. **Mark as Delivered**
```bash
PUT /orders/delivered/{order_id}
Authorization: Bearer {token}
```

#### 6. **Reject Order**
```bash
PUT /orders/reject/{order_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "rejection_reason": "Out of stock"
}
```

---

## 📊 Sample Order Data

### Customer Names:
- Rajesh Kumar
- Priya Sharma
- Amit Patel
- Sneha Reddy
- Vikram Singh
- And 5 more...

### Order Details:
- **Items per order:** 1-4 menu items
- **Total amounts:** ₹147 - ₹568
- **Delivery fee:** ₹30 (standard)
- **Tax:** 5% of subtotal
- **Payment methods:** Cash, Card, UPI, Wallet
- **Special instructions:** Various (spicy, no onions, etc.)

---

## 🧪 Testing the Flow

### Step 1: Get New Orders
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/orders/new
```

### Step 2: Accept an Order
```bash
curl -X PUT \
  -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/orders/accept/1
```

### Step 3: Mark as Preparing
```bash
curl -X PUT \
  -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/orders/preparing/1
```

### Step 4: Mark as Ready
```bash
curl -X PUT \
  -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/orders/ready/1
```

### Step 5: Check Ongoing Orders
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/orders/ongoing
```

---

## 📱 Flutter Integration Example

```dart
// Load new orders
Future<List<Order>> loadNewOrders() async {
  final response = await http.get(
    Uri.parse('$baseUrl/orders/new'),
    headers: {'Authorization': 'Bearer $token'},
  );
  
  if (response.statusCode == 200) {
    final data = json.decode(response.body);
    final orders = data['data']['orders'] as List;
    return orders.map((o) => Order.fromJson(o)).toList();
  }
  
  throw Exception('Failed to load orders');
}

// Accept order
Future<void> acceptOrder(int orderId) async {
  final response = await http.put(
    Uri.parse('$baseUrl/orders/accept/$orderId'),
    headers: {'Authorization': 'Bearer $token'},
  );
  
  if (response.statusCode == 200) {
    print('Order accepted successfully');
  }
}

// Update order status
Future<void> updateOrderStatus(int orderId, String status) async {
  final endpoints = {
    'preparing': '/orders/preparing/$orderId',
    'ready': '/orders/ready/$orderId',
    'pickedup': '/orders/pickedup/$orderId',
    'delivered': '/orders/delivered/$orderId',
  };
  
  final response = await http.put(
    Uri.parse('$baseUrl${endpoints[status]}'),
    headers: {'Authorization': 'Bearer $token'},
  );
  
  if (response.statusCode == 200) {
    print('Order status updated to $status');
  }
}
```

---

## 🎯 Order Statistics

Run this to see your order breakdown:

```bash
# Count orders by status
sqlite3 fastfoodie.db "SELECT status, COUNT(*) as count FROM orders GROUP BY status;"
```

**Expected Output:**
```
new|5
accepted|2
preparing|2
ready|2
picked_up|2
delivered|14
rejected|1
```

---

## 🔔 WebSocket Support (Real-time Updates)

The orders router also includes WebSocket support for real-time order updates:

```javascript
// Connect to WebSocket
const ws = new WebSocket('ws://localhost:8000/orders/ws/live?token=YOUR_TOKEN');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('New order update:', data);
  
  if (data.event === 'new_order') {
    // Show notification for new order
    showNotification(data.order);
  }
};
```

---

## ✅ Summary

| Endpoint | Purpose | Status Filter |
|----------|---------|---------------|
| `/orders/new` | New orders | `NEW` |
| `/orders/ongoing` | Active orders | `ACCEPTED`, `PREPARING`, `READY`, `PICKED_UP` |
| `/orders/completed` | Finished orders | `DELIVERED`, `REJECTED`, `CANCELLED` |
| `/orders/details/{id}` | Full order details | Any |
| `/orders/accept/{id}` | Accept order | `NEW` → `ACCEPTED` |
| `/orders/preparing/{id}` | Start cooking | `ACCEPTED` → `PREPARING` |
| `/orders/ready/{id}` | Ready for pickup | `PREPARING` → `READY` |
| `/orders/pickedup/{id}` | Picked up | `READY` → `PICKED_UP` |
| `/orders/delivered/{id}` | Delivered | `PICKED_UP` → `DELIVERED` |
| `/orders/reject/{id}` | Reject order | `NEW` → `REJECTED` |

---

## 🚀 Next Steps

1. **Test all endpoints** using the examples above
2. **Integrate with Flutter app** using the code samples
3. **Test the order flow** by moving orders through different statuses
4. **Set up WebSocket** for real-time notifications

---

**Your orders are ready to use!** 🎉

**Server:** http://localhost:8000  
**Docs:** http://localhost:8000/docs  
**Orders:** 28 realistic orders seeded
