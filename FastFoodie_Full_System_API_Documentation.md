# FastFoodie Full System API Documentation

This document outlines the complete API reference for both the **Owner App** and **Customer App**, covering the verified end-to-end flow.

**Base URL**: `http://<your-server-ip>:8000`

---

# 📱 PART 1: OWNER APP APIs

## 1. Authentication

### 1.1 Send OTP
*   **Endpoint**: `/auth/send-otp`
*   **Method**: `POST`
*   **Request**:
    ```json
    {
      "phone_number": "+919988776655",
      "role": "owner"
    }
    ```
*   **Response**:
    ```json
    {
      "success": true,
      "data": { "otp": "123456", ... }
    }
    ```

### 1.2 Verify OTP (Login/Register)
*   **Endpoint**: `/auth/verify-otp`
*   **Method**: `POST`
*   **Request**:
    ```json
    {
      "phone_number": "+919988776655",
      "otp_code": "123456",
      "role": "owner"
    }
    ```
*   **Response**:
    ```json
    {
      "access_token": "eyJhbGci...",
      "token_type": "bearer",
      "owner": { "id": 1, "full_name": "...", ... }
    }
    ```

## 2. Restaurant Management

### 2.1 Create Restaurant
*   **Endpoint**: `/restaurant/create`
*   **Method**: `POST`
*   **Header**: `Authorization: Bearer <owner_token>`
*   **Request**:
    ```json
    {
      "restaurant_name": "Spice Garden",
      "restaurant_type": "restaurant",
      "fssai_license_number": "12345678901234",
      "opening_time": "09:00",
      "closing_time": "23:00"
    }
    ```
*   **Response**:
    ```json
    {
      "success": true,
      "data": { "id": 1, "restaurant_name": "Spice Garden", ... }
    }
    ```

### 2.2 Open/Close Restaurant
*   **Endpoint**: `/restaurant/status?is_open=true` (or `false`)
*   **Method**: `PUT`
*   **Header**: `Authorization: Bearer <owner_token>`
*   **Response**:
    ```json
    {
      "success": true,
      "message": "Restaurant is now opened",
      "data": { "is_open": true }
    }
    ```

## 3. Menu Management

### 3.1 Get Categories
*   **Endpoint**: `/menu/categories`
*   **Method**: `GET`
*   **Header**: `Authorization: Bearer <owner_token>`
*   **Response**:
    ```json
    {
      "success": true,
      "data": {
        "categories": [ { "id": 1, "name": "Starters", ... } ]
      }
    }
    ```

### 3.2 Add Menu Item
*   **Endpoint**: `/menu/item/add`
*   **Method**: `POST`
*   **Header**: `Authorization: Bearer <owner_token>`
*   **Request**:
    ```json
    {
      "name": "Paneer Tikka",
      "description": "Spicy cottage cheese",
      "price": 250.00,
      "category_id": 1,
      "is_vegetarian": true,
      "is_available": true,
      "preparation_time": 15
    }
    ```
*   **Response**:
    ```json
    {
      "success": true,
      "data": { "id": 101, "name": "Paneer Tikka", ... }
    }
    ```

## 4. Order Management (Fulfillment)

### 4.1 Get New Orders
*   **Endpoint**: `/orders/new`
*   **Method**: `GET`
*   **Header**: `Authorization: Bearer <owner_token>`
*   **Response**:
    ```json
    {
      "success": true,
      "data": {
        "orders": [
          {
            "order_id": 501,
            "item_count": 2,
            "total_amount": 500.00,
            "status": "new",
            ...
          }
        ]
      }
    }
    ```

### 4.2 Accept Order
*   **Endpoint**: `/orders/{order_id}/accept`
*   **Method**: `PUT`
*   **Header**: `Authorization: Bearer <owner_token>`
*   **Response**:
    ```json
    {
      "success": true,
      "message": "Order marked as accepted"
    }
    ```

### 4.3 Mark Ready
*   **Endpoint**: `/orders/{order_id}/ready`
*   **Method**: `PUT`
*   **Header**: `Authorization: Bearer <owner_token>`

### 4.4 Mark Picked Up (Out for Delivery)
*   **Endpoint**: `/orders/{order_id}/pickedup`
*   **Method**: `PUT`
*   **Header**: `Authorization: Bearer <owner_token>`

---

# 🛒 PART 2: CUSTOMER APP APIs

## 1. Authentication

### 1.1 Send OTP
*   **Endpoint**: `/customer/auth/send-otp`
*   **Method**: `POST`
*   **Request**:
    ```json
    {
      "phone_number": "+917766554433"
    }
    ```

### 1.2 Verify OTP
*   **Endpoint**: `/customer/auth/verify-otp`
*   **Method**: `POST`
*   **Request**:
    ```json
    {
      "phone_number": "+917766554433",
      "otp_code": "123456"
    }
    ```
*   **Response**: Returns `access_token` for customer.

## 2. Discovery

### 2.1 Get Home Data
*   **Endpoint**: `/customer/home`
*   **Method**: `GET`
*   **Header**: `Authorization: Bearer <customer_token>`
*   **Response**:
    ```json
    {
      "success": true,
      "data": {
        "categories": [...],
        "restaurants": [
          { "id": 1, "restaurant_name": "Spice Garden", "is_open": true, ... }
        ],
        "offers": [...]
      }
    }
    ```

## 3. Address & Cart

### 3.1 Add Address
*   **Endpoint**: `/customer/addresses`
*   **Method**: `POST`
*   **Header**: `Authorization: Bearer <customer_token>`
*   **Request**:
    ```json
    {
      "latitude": 12.9716,
      "longitude": 77.5946,
      "address_line_1": "Flat 101",
      "city": "Bangalore",
      "state": "KA",
      "pincode": "560001",
      "is_default": true
    }
    ```

### 3.2 Add to Cart
*   **Endpoint**: `/customer/cart/add`
*   **Method**: `POST`
*   **Header**: `Authorization: Bearer <customer_token>`
*   **Request**:
    ```json
    {
      "menu_item_id": 101,
      "quantity": 2,
      "restaurant_id": 1
    }
    ```

## 4. Order Placement & Tracking

### 4.1 Place Order
*   **Endpoint**: `/customer/orders`
*   **Method**: `POST`
*   **Header**: `Authorization: Bearer <customer_token>`
*   **Request**:
    ```json
    {
      "restaurant_id": 1,
      "address_id": 5,
      "payment_method": "UPI"
    }
    ```
*   **Response**:
    ```json
    {
      "success": true,
      "data": { "order_id": 501, "order_number": "ORD..." }
    }
    ```

### 4.2 Track Order
*   **Endpoint**: `/customer/orders/{order_id}/track`
*   **Method**: `GET`
*   **Header**: `Authorization: Bearer <customer_token>`
*   **Response**:
    ```json
    {
      "success": true,
      "data": {
        "order_id": 501,
        "status": "accepted",  // updates to "preparing", "picked_up", etc.
        "estimated_arrival_time": "30 min",
        "timeline": [
          { "title": "Order Confirmed", "is_completed": true, ... },
          { "title": "Preparing", "is_current": true, ... }
        ],
        "delivery_partner": null, // Populates when status is picked_up
        "items": [...]
      }
    }
    ```
