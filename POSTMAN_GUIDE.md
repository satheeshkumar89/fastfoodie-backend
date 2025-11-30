# FastFoodie API - Postman Collection Guide

## 📦 Import the Collection

1. Open Postman
2. Click **Import** button (top left)
3. Select `FastFoodie_API_Collection.json`
4. Collection will appear in your workspace

## 🔧 Setup

### Configure Variables
The collection uses variables for easy testing:

| Variable | Default Value | Description |
|----------|--------------|-------------|
| `base_url` | `http://localhost:8000` | API base URL |
| `access_token` | (auto-set) | JWT token from login |
| `phone_number` | `+918668198712` | Test phone number |
| `otp_code` | (auto-set) | OTP from send-otp |

**To modify variables:**
1. Click on the collection name
2. Go to **Variables** tab
3. Update values as needed

## 🚀 Quick Start Guide

### Step 1: Authentication Flow

#### 1.1 Send OTP
```
POST /auth/send-otp
```
- No authentication required
- OTP is automatically saved to `{{otp_code}}` variable
- In development mode, OTP is returned in response

**Response:**
```json
{
  "success": true,
  "message": "OTP sent successfully",
  "data": {
    "phone_number": "+918668198712",
    "expires_in": "5 minutes",
    "otp": "123456",
    "note": "OTP included in response for development only"
  }
}
```

#### 1.2 Verify OTP
```
POST /auth/verify-otp
```
- Uses `{{otp_code}}` from previous request
- Access token is automatically saved to `{{access_token}}`
- All subsequent requests will use this token

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "owner": {
    "id": 1,
    "full_name": "",
    "email": "",
    "phone_number": "+918668198712",
    "is_active": true
  }
}
```

### Step 2: Test Protected Endpoints

All other endpoints require authentication. The collection is configured to automatically use the `{{access_token}}` variable.

## 📚 API Endpoints

### Authentication (No Auth Required)
- ✅ `POST /auth/send-otp` - Send OTP to phone
- ✅ `POST /auth/verify-otp` - Verify OTP and get token
- ✅ `POST /auth/resend-otp` - Resend OTP

### Dashboard (Auth Required)
- ✅ `GET /dashboard/today-summary` - Today's stats with growth
- ✅ `GET /dashboard/quick-actions` - Quick action buttons
- ✅ `GET /dashboard/overview` - Complete dashboard data

### Orders (Auth Required)
- ✅ `GET /orders/new` - Get new orders
- ✅ `GET /orders/ongoing` - Get ongoing orders
- ✅ `GET /orders/completed` - Get completed orders
- ✅ `GET /orders/{id}` - Get order details
- ✅ `PUT /orders/{id}/accept` - Accept order
- ✅ `PUT /orders/{id}/preparing` - Mark as preparing
- ✅ `PUT /orders/{id}/ready` - Mark as ready
- ✅ `PUT /orders/{id}/pickedup` - Mark as picked up
- ✅ `PUT /orders/{id}/delivered` - Mark as delivered
- ✅ `POST /orders/{id}/reject` - Reject order

### Menu Management (Auth Required)
- ✅ `GET /menu/categories` - Get all categories
- ✅ `GET /menu/items` - Get all menu items
- ✅ `GET /menu/items?category_id=X` - Filter by category
- ✅ `POST /menu/item/add` - Add new menu item
- ✅ `PUT /menu/item/update/{id}` - Update menu item
- ✅ `DELETE /menu/item/{id}` - Delete menu item
- ✅ `PUT /menu/item/availability/{id}` - Toggle availability
- ✅ `PUT /menu/item/out-of-stock/{id}` - Mark out of stock
- ✅ `POST /menu/item/duplicate/{id}` - Duplicate item

### Owner Profile (Auth Required)
- ✅ `GET /owner/profile` - Get owner profile
- ✅ `PUT /owner/profile` - Update owner profile

### Restaurant (Auth Required)
- ✅ `GET /restaurant/types` - Get restaurant types
- ✅ `GET /restaurant/my-restaurant` - Get my restaurant
- ✅ `POST /restaurant/create` - Create restaurant
- ✅ `PUT /restaurant/update` - Update restaurant
- ✅ `PUT /restaurant/toggle-status` - Open/Close restaurant

### Health Check (No Auth)
- ✅ `GET /health` - Server health status

## 🧪 Testing Workflow

### Complete Flow Example:

1. **Authenticate**
   ```
   1. Send OTP → Copy OTP from response
   2. Verify OTP → Token saved automatically
   ```

2. **Setup Restaurant**
   ```
   3. Create Restaurant
   4. Update Restaurant Profile
   5. Toggle Restaurant Status (Open)
   ```

3. **Manage Menu**
   ```
   6. Add Menu Item (Pizza)
   7. Add Menu Item (Burger)
   8. Get All Menu Items
   9. Update Menu Item
   10. Duplicate Menu Item
   ```

4. **Handle Orders**
   ```
   11. Get New Orders
   12. Accept Order
   13. Mark as Preparing
   14. Mark as Ready
   15. Mark as Picked Up
   16. Mark as Delivered
   ```

5. **View Dashboard**
   ```
   17. Get Today Summary
   18. Get Dashboard Overview
   ```

## 🔄 Auto-Save Features

The collection includes scripts that automatically:
- Save OTP from send-otp response
- Save access token from verify-otp response
- Use saved token for all authenticated requests

## 📝 Example Requests

### Add Menu Item
```json
{
  "name": "Margherita Pizza",
  "description": "Classic pizza with tomato sauce, mozzarella, and basil",
  "price": 299.00,
  "discount_price": 249.00,
  "image_url": "https://example.com/pizza.jpg",
  "category": "Main Course",
  "is_vegetarian": true,
  "is_available": true,
  "preparation_time": 20
}
```

### Update Item Availability
```json
{
  "is_available": false
}
```

### Reject Order
```json
{
  "status": "rejected",
  "rejection_reason": "Out of ingredients"
}
```

## 🌐 Environment Setup

### Local Development
```
base_url: http://localhost:8000
```

### Production
```
base_url: https://api.fastfoodie.com
```

To switch environments:
1. Create new environment in Postman
2. Set `base_url` variable
3. Select environment from dropdown

## 🔐 Authentication Notes

- Token expires in 30 minutes (configurable)
- After expiration, re-run verify-otp
- Token is sent as: `Authorization: Bearer {{access_token}}`
- Collection handles this automatically

## 🐛 Troubleshooting

### "Unauthorized" Error
- Run Send OTP → Verify OTP again
- Check if token is saved in variables
- Ensure server is running

### "Invalid OTP" Error
- OTP expires in 5 minutes
- Request new OTP
- Check OTP value in variables

### Connection Refused
- Ensure server is running: `uvicorn app.main:app --reload`
- Check `base_url` variable
- Verify port 8000 is not in use

## 📊 Response Format

All endpoints return standardized responses:

**Success:**
```json
{
  "success": true,
  "message": "Operation successful",
  "data": { ... }
}
```

**Error:**
```json
{
  "detail": "Error message"
}
```

## 🎯 Testing Tips

1. **Use Folders**: Requests are organized by feature
2. **Run in Order**: Follow the authentication flow first
3. **Check Console**: View auto-saved variables
4. **Use Examples**: Each request has sample data
5. **Modify IDs**: Update order/item IDs as needed

## 📱 WebSocket Testing

For real-time order updates, use a WebSocket client:
```
ws://localhost:8000/orders/live?token={{access_token}}
```

Events received:
- `new_order` - New order assigned
- `order_accepted` - Order accepted
- `preparing` - Order being prepared
- `ready` - Order ready for pickup
- `pickedup` - Order picked up
- `delivered` - Order delivered

## 🚀 Next Steps

1. Import collection
2. Run authentication flow
3. Test each endpoint
4. Integrate with your app
5. Deploy to production

## 📞 Support

For issues or questions:
- Check API docs: http://localhost:8000/docs
- View Swagger UI for interactive testing
- Check server logs for errors

---

**Happy Testing! 🎉**
