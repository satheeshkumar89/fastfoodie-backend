# FastFoodie Customer App API Documentation

This document outlines the End-to-End API flow for the FastFoodie Customer Application.

**Base URL**: `http://<your-server-ip>:8000`
**Authentication**: All endpoints (except Auth) require a Bearer Token in the header: `Authorization: Bearer <access_token>`

---

## 1. Authentication

### 1.1 Send OTP
*   **Endpoint**: `/customer/auth/send-otp`
*   **Method**: `POST`
*   **Description**: Sends a 6-digit OTP to the customer's phone number.
*   **Request Body**:
    ```json
    {
      "phone_number": "+919876543210"
    }
    ```
*   **Response**:
    ```json
    {
      "success": true,
      "message": "OTP sent successfully",
      "data": {
        "phone_number": "+919876543210",
        "expires_in": "5 minutes",
        "otp": "123456" // Only in development mode
      }
    }
    ```

### 1.2 Verify OTP
*   **Endpoint**: `/customer/auth/verify-otp`
*   **Method**: `POST`
*   **Description**: Verifies the OTP and returns an access token. Creates a new customer account if the phone number is new.
*   **Request Body**:
    ```json
    {
      "phone_number": "+919876543210",
      "otp_code": "123456"
    }
    ```
*   **Response**:
    ```json
    {
      "access_token": "eyJhbGciOiJIUzI1Ni...",
      "token_type": "bearer",
      "customer": {
        "id": 1,
        "full_name": null,
        "email": null,
        "phone_number": "+919876543210",
        "profile_photo": null,
        "is_active": true,
        "created_at": "2023-10-27T10:00:00"
      }
    }
    ```

### 1.3 Logout
*   **Endpoint**: `/customer/auth/logout`
*   **Method**: `POST`
*   **Description**: Logs out the customer (client-side token removal).
*   **Response**:
    ```json
    {
      "success": true,
      "message": "Logged out successfully"
    }
    ```

---

## 2. Profile Management

### 2.1 Get Profile
*   **Endpoint**: `/customer/profile`
*   **Method**: `GET`
*   **Description**: Fetches the current customer's profile details.
*   **Response**:
    ```json
    {
      "id": 1,
      "full_name": "John Doe",
      "email": "john@example.com",
      "phone_number": "+919876543210",
      "profile_photo": "https://example.com/photo.jpg",
      "is_active": true,
      "created_at": "..."
    }
    ```

### 2.2 Update Profile
*   **Endpoint**: `/customer/profile`
*   **Method**: `PUT`
*   **Description**: Updates customer details.
*   **Request Body**:
    ```json
    {
      "full_name": "John Doe",
      "email": "john@example.com",
      "profile_photo": "https://example.com/new_photo.jpg"
    }
    ```
*   **Response**: Returns the updated Customer object (same as Get Profile).

---

## 3. Home & Discovery

### 3.1 Get Home Data
*   **Endpoint**: `/customer/home`
*   **Method**: `GET`
*   **Description**: Fetches data for the home screen, including categories, active restaurants, and offers.
*   **Response**:
    ```json
    {
      "success": true,
      "data": {
        "categories": [
          { "id": 1, "name": "Pizza", "icon": "...", "display_order": 1 }
        ],
        "restaurants": [
          { "id": 1, "restaurant_name": "Spice Garden", "rating": 4.5, "is_open": true, ... }
        ],
        "offers": [...]
      }
    }
    ```

### 3.2 Get Restaurant Details
*   **Endpoint**: `/customer/restaurants/{restaurant_id}`
*   **Method**: `GET`
*   **Description**: Fetches comprehensive details for a specific restaurant, including its menu and reviews.
*   **Response**:
    ```json
    {
      "success": true,
      "data": {
        "id": 1,
        "restaurant_name": "Spice Garden",
        "address": { ... },
        "cuisines": [...],
        "menu": [
          { "id": 101, "name": "Paneer Tikka", "price": 250, "is_vegetarian": true, ... }
        ],
        "reviews": [...]
      }
    }
    ```

---

## 4. Address Management

### 4.1 Add Address
*   **Endpoint**: `/customer/addresses`
*   **Method**: `POST`
*   **Description**: Saves a new delivery address.
*   **Request Body**:
    ```json
    {
      "latitude": 12.9716,
      "longitude": 77.5946,
      "address_line_1": "Flat 402, Sunshine Apts",
      "city": "Bangalore",
      "state": "Karnataka",
      "pincode": "560001",
      "address_type": "home",
      "is_default": true
    }
    ```
*   **Response**:
    ```json
    {
      "success": true,
      "data": { "id": 5, ... }
    }
    ```

### 4.2 Get Addresses
*   **Endpoint**: `/customer/addresses`
*   **Method**: `GET`
*   **Description**: Fetches all saved addresses.
*   **Response**:
    ```json
    {
      "success": true,
      "data": [ { "id": 5, "address_line_1": "...", ... } ]
    }
    ```

---

## 5. Cart & Order Management

### 5.1 Add to Cart
*   **Endpoint**: `/customer/cart/add`
*   **Method**: `POST`
*   **Description**: Adds an item to the cart. Fails if items from another restaurant exist.
*   **Request Body**:
    ```json
    {
      "menu_item_id": 101,
      "quantity": 1,
      "restaurant_id": 1
    }
    ```
*   **Response**:
    ```json
    {
      "success": true,
      "data": {
        "id": 1,
        "restaurant_name": "Spice Garden",
        "items": [...],
        "item_total": 250,
        "delivery_fee": 40,
        "tax_amount": 12.5,
        "total_amount": 302.5
      }
    }
    ```

### 5.2 Get Cart
*   **Endpoint**: `/customer/cart`
*   **Method**: `GET`
*   **Description**: Fetches current cart state and bill details.
*   **Response**: Same structure as Add to Cart response.

### 5.3 Update Cart Item
*   **Endpoint**: `/customer/cart/items/{item_id}`
*   **Method**: `PUT`
*   **Description**: Updates quantity of a specific cart item.
*   **Request Body**: `{"quantity": 2}`
*   **Response**: Updated Cart object.

### 5.4 Remove Cart Item
*   **Endpoint**: `/customer/cart/items/{item_id}`
*   **Method**: `DELETE`
*   **Description**: Removes an item from the cart.
*   **Response**: Updated Cart object.

### 5.5 Create Order (Checkout)
*   **Endpoint**: `/customer/orders`
*   **Method**: `POST`
*   **Description**: Places an order using the current cart.
*   **Request Body**:
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
      "message": "Order placed successfully",
      "data": {
        "order_id": 123,
        "order_number": "ORD83729"
      }
    }
    ```

### 5.6 Get Order History
*   **Endpoint**: `/customer/orders`
*   **Method**: `GET`
*   **Description**: Fetches list of past orders.
*   **Response**: List of Order objects.

### 5.7 Track Order
*   **Endpoint**: `/customer/orders/{order_id}/track`
*   **Method**: `GET`
*   **Description**: Fetches real-time tracking details.
*   **Response**:
    ```json
    {
      "success": true,
      "data": {
        "order_id": 123,
        "status": "preparing",
        "estimated_arrival_time": "30 min",
        "timeline": [
          { "title": "Order Confirmed", "is_completed": true, ... },
          { "title": "Preparing", "is_current": true, ... }
        ],
        "delivery_partner": null,
        "items": [...]
      }
    }
    ```
