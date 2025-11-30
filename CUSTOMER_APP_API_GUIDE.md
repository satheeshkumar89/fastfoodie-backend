# Customer App API Guide

## Authentication

### 1. Send OTP
- **Endpoint**: `POST /customer/auth/send-otp`
- **Description**: Sends a 6-digit OTP to the provided phone number.
- **Request Body**:
  ```json
  {
    "phone_number": "+919876543210"
  }
  ```
- **Response**:
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

### 2. Verify OTP
- **Endpoint**: `POST /customer/auth/verify-otp`
- **Description**: Verifies the OTP and returns an access token. If the user is new, a minimal account is created.
- **Request Body**:
  ```json
  {
    "phone_number": "+919876543210",
    "otp_code": "123456"
  }
  ```
- **Response**:
  ```json
  {
    "access_token": "eyJhbG...",
    "token_type": "bearer",
    "customer": {
      "id": 1,
      "full_name": null, // null for new users
      "email": null,
      "phone_number": "+919876543210",
      "profile_photo": null,
      "is_active": true,
      "created_at": "2023-10-27T10:00:00"
    }
  }
  ```

## Profile Management

### 3. Update Profile
- **Endpoint**: `PUT /customer/profile`
- **Description**: Updates customer details (Name, Email, Profile Photo). Call this after "Create Account" screen.
- **Headers**: `Authorization: Bearer <access_token>`
- **Request Body**:
  ```json
  {
    "full_name": "Satheesh Kumar",
    "email": "sathesitc@gmail.com",
    "profile_photo": "https://example.com/photo.jpg" // Optional
  }
  ```
- **Response**: Updated Customer object.

### 4. Get Profile
- **Endpoint**: `GET /customer/profile`
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**: Customer object.

## Home & Discovery

### 5. Get Home Data
- **Endpoint**: `GET /customer/home`
- **Description**: Returns data for the home screen including categories, restaurants, and offers.
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**:
  ```json
  {
    "success": true,
    "data": {
      "categories": [...],
      "restaurants": [...],
      "offers": [...]
    }
  }
  ```

### 6. Get Restaurant Details
- **Endpoint**: `GET /customer/restaurants/{restaurant_id}`
- **Description**: Returns full restaurant details including menu, reviews, and info.
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**:
  ```json
  {
    "success": true,
    "data": {
      "id": 1,
      "restaurant_name": "Spice Garden",
      "average_rating": 4.5,
      "opening_time": "11:00",
      "closing_time": "23:00",
      "cost_for_two": 400,
      "description": "Experience authentic flavors...",
      "address": {
        "address_line_1": "123 MG Road",
        "city": "Bangalore",
        ...
      },
      "cuisines": [
        {"name": "North Indian"},
        {"name": "Chinese"}
      ],
      "menu": [
        {
          "id": 101,
          "name": "Paneer Butter Masala",
          "price": 280,
          "is_bestseller": true,
          "rating": 4.6,
          ...
        }
      ],
      "reviews": [
        {
          "id": 1,
          "customer_name": "Priya Sharma",
          "rating": 5,
          "review_text": "Absolutely loved the food!",
          "created_at": "..."
        }
      ]
    }
  }
  ```

## Cart Management

### 7. Add to Cart
- **Endpoint**: `POST /customer/cart/add`
- **Description**: Add an item to the cart. If items from another restaurant exist, it will return an error (or handle as per logic).
- **Headers**: `Authorization: Bearer <access_token>`
- **Request Body**:
  ```json
  {
    "menu_item_id": 101,
    "quantity": 1,
    "restaurant_id": 1
  }
  ```
- **Response**: Returns updated Cart object.

### 8. Get Cart
- **Endpoint**: `GET /customer/cart`
- **Description**: Get current cart details with bill summary.
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**:
  ```json
  {
    "success": true,
    "data": {
      "id": 1,
      "restaurant_id": 1,
      "restaurant_name": "Spice Garden",
      "items": [
        {
          "id": 5,
          "menu_item_id": 101,
          "menu_item": { ... },
          "quantity": 2,
          "price": 280
        }
      ],
      "item_total": 560,
      "delivery_fee": 40,
      "tax_amount": 28,
      "discount_amount": 0,
      "total_amount": 628
    }
  }
  ```

### 9. Update Cart Item
- **Endpoint**: `PUT /customer/cart/items/{item_id}`
- **Description**: Update quantity of a specific cart item. Set quantity to 0 to remove.
- **Headers**: `Authorization: Bearer <access_token>`
- **Request Body**:
  ```json
  {
    "quantity": 3
  }
  ```
- **Response**: Updated Cart object.

### 10. Remove Cart Item
- **Endpoint**: `DELETE /customer/cart/items/{item_id}`
- **Description**: Remove an item from the cart.
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**: Updated Cart object.

## Order Management

### 11. Create Order (Checkout)
- **Endpoint**: `POST /customer/orders`
- **Description**: Place an order using the current cart items.
- **Headers**: `Authorization: Bearer <access_token>`
- **Request Body**:
  ```json
  {
    "restaurant_id": 1,
    "address_id": 1, // ID of the selected address
    "payment_method": "UPI" // UPI, Cards, Net Banking, Cash on Delivery
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "message": "Order placed successfully",
    "data": {
      "order_id": 123,
      "order_number": "ORD12345ABC"
    }
  }
  ```

### 12. Get Order History
- **Endpoint**: `GET /customer/orders`
- **Description**: Returns all past orders for the customer.
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**: List of Order objects with restaurant details.

### 13. Repeat Order
- **Endpoint**: `POST /customer/orders/{order_id}/repeat`
- **Description**: Adds items from a past order to the cart. Clears existing cart if restaurant differs.
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**: Updated Cart object.

## Address Management

### 14. Add Address
- **Endpoint**: `POST /customer/addresses`
- **Description**: Save a new delivery address.
- **Headers**: `Authorization: Bearer <access_token>`
- **Request Body**:
  ```json
  {
    "latitude": 12.9716,
    "longitude": 77.5946,
    "address_line_1": "Flat 402, Sunshine Apts",
    "address_line_2": "MG Road",
    "city": "Bangalore",
    "state": "Karnataka",
    "pincode": "560001",
    "landmark": "Near Metro Station",
    "address_type": "home", // home, work, other
    "is_default": true
  }
  ```
- **Response**: Created Address object.

### 15. Get Addresses
- **Endpoint**: `GET /customer/addresses`
- **Description**: Get all saved addresses.
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**: List of Address objects.

### 16. Update Address
- **Endpoint**: `PUT /customer/addresses/{address_id}`
- **Description**: Update an existing address.
- **Headers**: `Authorization: Bearer <access_token>`
- **Request Body**: Same as Add Address.
- **Response**: Updated Address object.

### 17. Delete Address
- **Endpoint**: `DELETE /customer/addresses/{address_id}`
- **Description**: Delete an address.
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**: Success message.
  
## Order Tracking

### 18. Track Order
- **Endpoint**: `GET /customer/orders/{order_id}/track`
- **Description**: Get detailed tracking info including timeline, delivery partner, and bill details.
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**:
  ```json
  {
    "success": true,
    "data": {
      "order_id": 123,
      "order_number": "ORD123",
      "status": "picked_up",
      "estimated_arrival_time": "14 min",
      "delivery_partner": {
        "id": 999,
        "full_name": "Rajesh Kumar",
        "phone_number": "+919876543210",
        "vehicle_number": "DL 01 AB 1234",
        "rating": 4.8,
        "profile_photo": "..."
      },
      "timeline": [
        {
          "title": "Order Confirmed",
          "subtitle": "...",
          "time": "07:04 PM",
          "is_completed": true,
          "is_current": false
        },
        ...
      ],
      "restaurant_name": "Spice Garden",
      "items": [...],
      "item_total": 350,
      "delivery_fee": 40,
      "tax_amount": 17.5,
      "discount_amount": 0,
      "total_amount": 407.5
    }
  }
  ```



