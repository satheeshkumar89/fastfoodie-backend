# 🚴 Delivery Partner API Documentation

Complete API documentation for FastFoodie Delivery Partner App

## Base URL
```
Production: https://dharaifooddelivery.in
Development: http://localhost:8000
```

## Authentication
All authenticated endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <access_token>
```

---

## 📱 Authentication APIs

### 1. Send OTP
Send OTP to delivery partner's phone number. Creates delivery partner account if doesn't exist.

**Endpoint:** `POST /delivery-partner/auth/send-otp`

**Request Body:**
```json
{
  "phone_number": "+919876543210"
}
```

**Response:**
```json
{
  "success": true,
  "message": "OTP sent successfully",
  "data": {
    "phone_number": "+919876543210",
    "expires_in": "5 minutes",
    "otp": "123456",  // Only in development mode
    "note": "OTP included in response for development only"
  }
}
```

---

### 2. Verify OTP & Login
Verify OTP and get JWT access token.

**Endpoint:** `POST /delivery-partner/auth/verify-otp`

**Request Body:**
```json
{
  "phone_number": "+919876543210",
  "otp_code": "123456"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "delivery_partner": {
    "id": 1,
    "full_name": "Delivery Partner",
    "phone_number": "+919876543210",
    "vehicle_number": null,
    "rating": 5.0,
    "profile_photo": null
  }
}
```

---

## 👤 Profile APIs

###  3. Get Profile
Get delivery partner's profile.

**Endpoint:** `GET /delivery-partner/profile`
**Auth:** Required

**Response:**
```json
{
  "id": 1,
  "full_name": "Rajesh Kumar",
  "phone_number": "+919876543210",
  "vehicle_number": "KA01AB1234",
  "rating": 4.8,
  "profile_photo": "https://s3.amazonaws.com/..."
}
```

---

### 4. Update Profile
Update delivery partner's profile.

**Endpoint:** `PUT /delivery-partner/profile`
**Auth:** Required

**Request Body:**
```json
{
  "full_name": "Rajesh Kumar",
  "vehicle_number": "KA01AB1234",
  "profile_photo": "https://s3.amazonaws.com/..."
}
```

**Response:**
```json
{
  "success": true,
  "message": "Profile updated successfully",
  "data": {
    "id": 1,
    "full_name": "Rajesh Kumar",
    "phone_number": "+919876543210",
    "vehicle_number": "KA01AB1234",
    "rating": 4.8,
    "profile_photo": "https://s3.amazonaws.com/..."
  }
}
```

---

## 🔔 Push Notifications

### 5. Register Device Token
Register FCM device token for push notifications.

**Endpoint:** `POST /delivery-partner/device-token`
**Auth:** Required

**Request Body:**
```json
{
  "token": "fcm_device_token_here...",
  "device_type": "android"  // or "ios", "web"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Device token registered successfully"
}
```

---

## 📦 Orders APIs

### 6. Get Available Orders
Get all orders that are READY for pickup.

**Endpoint:** `GET /delivery-partner/orders/available`
**Auth:** Required

**Response:**
```json
[
  {
    "id": 101,
    "order_number": "ORD20241224001",
    "restaurant_name": "Spice Kitchen",
    "customer_name": "Anita Sharma",
    "customer_phone": "+919123456789",
    "delivery_address": "123, MG Road, Bangalore, Karnataka 560001",
    "total_amount": 450.00,
    "status": "ready",
    "created_at": "2024-12-24T10:30:00Z",
    "estimated_delivery_time": "2024-12-24T11:15:00Z"
  }
]
```

---

### 7. Get Active Orders
Get all orders currently being delivered by this delivery partner.

**Endpoint:** `GET /delivery-partner/orders/active`
**Auth:** Required

**Response:**
```json
[
  {
    "id": 102,
    "order_number": "ORD20241224002",
    "restaurant_name": "Burger Joint",
    "customer_name": "Vikram Singh",
    "customer_phone": "+919876543210",
    "delivery_address": "45, Brigade Road, Bangalore, Karnataka 560025",
    "total_amount": 350.00,
    "status": "picked_up",
    "created_at": "2024-12-24T11:00:00Z",
    "estimated_delivery_time": "2024-12-24T11:45:00Z"
  }
]
```

---

### 8. Get Completed Orders
Get delivery history - all completed deliveries.

**Endpoint:** `GET /delivery-partner/orders/completed?limit=50`
**Auth:** Required

**Query Parameters:**
- `limit` (optional): Number of orders to fetch (default: 50)

**Response:**
```json
[
  {
    "id": 100,
    "order_number": "ORD20241223099",
    "restaurant_name": "Pizza Paradise",
    "customer_name": "Priya Mehta",
    "customer_phone": "+919111222333",
    "delivery_address": "78, Indiranagar, Bangalore, Karnataka 560038",
    "total_amount": 650.00,
    "status": "delivered",
    "created_at": "2024-12-23T20:15:00Z",
    "estimated_delivery_time": "2024-12-23T21:00:00Z"
  }
]
```

---

### 9. Get Order Details
Get detailed information about a specific order.

**Endpoint:** `GET /delivery-partner/orders/{order_id}`
**Auth:** Required

**Response:**
```json
{
  "id": 101,
  "order_number": "ORD20241224001",
  "restaurant_name": "Spice Kitchen",
  "restaurant_phone": "+919876500000",
  "restaurant_address": "12, MG Road, Bangalore",
  "customer_name": "Anita Sharma",
  "customer_phone": "+919123456789",
  "delivery_address": "123, MG Road, Bangalore, Karnataka 560001",
  "status": "ready",
  "total_amount": 450.00,
  "delivery_fee": 40.00,
  "payment_method": "UPI",
  "payment_status": "paid",
  "special_instructions": "Ring the doorbell twice",
  "items": [
    {
      "id": 1,
      "menu_item_id": 25,
      "quantity": 2,
      "price": 180.00,
      "special_instructions": "Extra spicy"
    }
  ],
  "created_at": "2024-12-24T10:30:00Z",
  "estimated_delivery_time": "2024-12-24T11:15:00Z"
}
```

---

### 10. Accept Order
Accept an order for delivery. Order must be in READY status.

**Endpoint:** `POST /delivery-partner/orders/{order_id}/accept`
**Auth:** Required

**Response:**
```json
{
  "success": true,
  "message": "Order accepted for delivery successfully",
  "data": {
    "order_id": 101,
    "status": "picked_up"
  }
}
```

**Notifications Sent:**
- ✅ Customer: "Order #ORD20241224001 Picked Up - Rajesh Kumar is on the way with your order!"
- ✅ Restaurant Owner: "Order #ORD20241224001 Picked Up - Delivery partner Rajesh Kumar has picked up the order"

---

### 11. Mark Order as Delivered
Complete the delivery. Order must be in PICKED_UP status.

**Endpoint:** `POST /delivery-partner/orders/{order_id}/complete`
**Auth:** Required

**Response:**
```json
{
  "success": true,
  "message": "Order marked as delivered successfully",
  "data": {
    "order_id": 101,
    "status": "delivered"
  }
}
```

**Notifications Sent:**
- ✅ Customer: "Order #ORD20241224001 Delivered - Your order has been delivered. Enjoy your meal! 🎉"
- ✅ Restaurant Owner: "Order #ORD20241224001 Delivered - Order has been successfully delivered to the customer"

---

## 💰 Earnings & Stats

### 12. Get Earnings
Get earnings statistics for the delivery partner.

**Endpoint:** `GET /delivery-partner/earnings`
**Auth:** Required

**Response:**
```json
{
  "today_earnings": 320.00,
  "week_earnings": 2450.00,
  "month_earnings": 8900.00,
  "total_deliveries": 247,
  "avg_rating": 4.8
}
```

---

## 🔔 Notifications

### 13. Get Notification History
Get all notifications for the delivery partner.

**Endpoint:** `GET /delivery-partner/notifications?limit=50`
**Auth:** Required

**Query Parameters:**
- `limit` (optional): Number of notifications to fetch (default: 50)

**Response:**
```json
[
  {
    "id": 1,
    "title": "New Order Available",
    "message": "Order #ORD20241224001 is ready for pickup from Spice Kitchen",
    "notification_type": "order_update",
    "order_id": 101,
    "is_read": false,
    "created_at": "2024-12-24T10:30:00Z"
  }
]
```

---

### 14. Mark Notification as Read
Mark a specific notification as read.

**Endpoint:** `PUT /delivery-partner/notifications/{notification_id}/read`
**Auth:** Required

**Response:**
```json
{
  "success": true,
  "message": "Notification marked as read"
}
```

---

## 📊 Order Flow

### Complete Order Lifecycle for Delivery Partner:

1. **Available Orders** (`status: ready`)
   - Order is ready for pickup at restaurant
   - Delivery partner can view available orders
   
2. **Accept Order** → `POST /delivery-partner/orders/{order_id}/accept`
   - Status changes to `picked_up`
   - Delivery partner assigned to order
   - Notifications sent to customer & restaurant
   
3. **Active Delivery** (`status: picked_up`)
   - Order appears in active orders
   - Delivery partner is on the way to customer
   
4. **Complete Delivery** → `POST /delivery-partner/orders/{order_id}/complete`
   - Status changes to `delivered`
   - Order moves to completed history
   - Notifications sent to customer & restaurant
   - Earnings updated

---

## 🔔 Push Notification Events

Delivery partners receive push notifications for:

1. **New Available Order**
   - When restaurant marks order as READY
   - Title: "New Order Available #ORD..."
   - Message: "Order is ready for pickup from [Restaurant]"

2. **Order Alerts**
   - Customer requests
   - Special instructions updates
   - Priority deliveries

---

## 🚀 Getting Started

### 1. Authentication Flow
```
1. User enters phone number → POST /delivery-partner/auth/send-otp
2. User enters OTP → POST /delivery-partner/auth/verify-otp
3. Receive access_token
4. Store token securely
5. Use token for all subsequent API calls
```

### 2. Register for Push Notifications
```
1. Get FCM device token from Firebase
2. POST /delivery-partner/device-token with token
3. Start receiving push notifications
```

### 3. Complete Profile
```
1. PUT /delivery-partner/profile
2. Update full_name, vehicle_number, profile_photo
```

### 4. Start Accepting Orders
```
1. GET /delivery-partner/orders/available
2. View order details → GET /delivery-partner/orders/{order_id}
3. Accept order → POST /delivery-partner/orders/{order_id}/accept
4. Navigate to restaurant
5. Pick up order
6. Navigate to customer
7. Complete delivery → POST /delivery-partner/orders/{order_id}/complete
```

---

## ⚠️ Error Responses

### 400 Bad Request
```json
{
  "detail": "Order is not ready for pickup. Current status: preparing"
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid or expired OTP"
}
```

### 403 Forbidden
```json
{
  "detail": "Your account has been deactivated. Please contact support."
}
```

### 404 Not Found
```json
{
  "detail": "Order not found"
}
```

---

## 📱 Flutter App Integration

Check `fastfoodie_delivery_partner_app/` directory for complete Flutter implementation with:
- ✅ Authentication (OTP)
- ✅ Profile Management
- ✅ Available Orders List
- ✅ Active Deliveries
- ✅ Delivery History
- ✅ Earnings Dashboard
- ✅ Push Notifications
- ✅ Real-time Order Updates
- ✅ Google Maps Integration
- ✅ Navigation to Restaurant/Customer

---

## 🎯 Key Features

✅ **OTP Authentication** - Secure phone-based login
✅ **Real-time Push Notifications** - Instant order alerts
✅ **Order Management** - Accept, pickup, deliver
✅ **Earnings Tracking** - Daily, weekly, monthly stats
✅ **Profile Management** - Update details, vehicle info
✅ **Order History** - Complete delivery records
✅ **Multi-device Support** - iOS, Android, Web

---

**Last Updated:** December 24, 2024
**API Version:** 1.0.0
