# API Testing Guide

This document provides example requests for testing all API endpoints.

## Authentication

### 1. Send OTP

```bash
curl -X POST "http://localhost:8000/auth/send-otp" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+919876543210"
  }'
```

### 2. Verify OTP

```bash
curl -X POST "http://localhost:8000/auth/verify-otp" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+919876543210",
    "otp_code": "123456"
  }'
```

**Save the `access_token` from the response for subsequent requests.**

## Owner Details

### 3. Create Owner Details

```bash
curl -X POST "http://localhost:8000/owner/details" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "full_name": "John Doe",
    "email": "john@example.com",
    "phone_number": "+919876543210"
  }'
```

## Restaurant Setup

### 4. Get Restaurant Types

```bash
curl -X GET "http://localhost:8000/restaurant/types" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 5. Create Restaurant Details

```bash
curl -X POST "http://localhost:8000/restaurant/details" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "restaurant_name": "Tasty Bites",
    "restaurant_type": "restaurant",
    "fssai_license_number": "12345678901234",
    "opening_time": "09:00",
    "closing_time": "22:00"
  }'
```

### 6. Get Available Cuisines

```bash
curl -X GET "http://localhost:8000/restaurant/cuisines/available" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 7. Add Cuisines to Restaurant

```bash
curl -X POST "http://localhost:8000/restaurant/cuisines" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "cuisine_ids": [1, 2, 4]
  }'
```

### 8. Add Restaurant Address

```bash
curl -X POST "http://localhost:8000/restaurant/address" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "latitude": 28.6139,
    "longitude": 77.2090,
    "address_line_1": "123 Main Street",
    "address_line_2": "Near City Center",
    "city": "New Delhi",
    "state": "Delhi",
    "pincode": "110001",
    "landmark": "Opposite Metro Station"
  }'
```

### 9. Get Presigned URL for Document Upload

```bash
curl -X POST "http://localhost:8000/restaurant/documents/presigned-url?document_type=fssai_license&filename=fssai.pdf&content_type=application/pdf" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 10. Upload File to S3 (using presigned URL)

```bash
# Use the upload_url from previous response
curl -X PUT "PRESIGNED_URL" \
  -H "Content-Type: application/pdf" \
  --upload-file /path/to/fssai.pdf
```

### 11. Confirm Document Upload

```bash
curl -X POST "http://localhost:8000/restaurant/documents/confirm-upload?document_type=fssai_license&file_key=FILE_KEY&filename=fssai.pdf" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 12. Submit KYC

```bash
curl -X POST "http://localhost:8000/restaurant/submit-kyc" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 13. Get Verification Status

```bash
curl -X GET "http://localhost:8000/restaurant/verification-status" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Dashboard

### 14. Get Today's Summary

```bash
curl -X GET "http://localhost:8000/dashboard/today-summary" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 15. Get Quick Actions

```bash
curl -X GET "http://localhost:8000/dashboard/quick-actions" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Menu Management

### 16. Add Menu Item

```bash
curl -X POST "http://localhost:8000/menu/add-item" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "name": "Butter Chicken",
    "description": "Creamy tomato-based curry with tender chicken",
    "price": 299.00,
    "category": "Main Course",
    "is_vegetarian": false,
    "is_available": true,
    "preparation_time": 20
  }'
```

### 17. Get All Menu Items

```bash
curl -X GET "http://localhost:8000/menu/items" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 18. Update Menu Item

```bash
curl -X PUT "http://localhost:8000/menu/update-item/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "price": 349.00,
    "is_available": true
  }'
```

### 19. Delete Menu Item

```bash
curl -X DELETE "http://localhost:8000/menu/delete-item/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Orders

### 20. Get New Orders

```bash
curl -X GET "http://localhost:8000/orders/new" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 21. Get Ongoing Orders

```bash
curl -X GET "http://localhost:8000/orders/ongoing" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 22. Get Completed Orders

```bash
curl -X GET "http://localhost:8000/orders/completed" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 23. Accept Order

```bash
curl -X POST "http://localhost:8000/orders/1/accept" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 24. Reject Order

```bash
curl -X POST "http://localhost:8000/orders/1/reject" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "status": "rejected",
    "rejection_reason": "Out of ingredients"
  }'
```

### 25. Update Order Status

```bash
curl -X PUT "http://localhost:8000/orders/1/update-status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "status": "preparing"
  }'
```

## WebSocket Connection

### 26. Connect to Live Orders (JavaScript)

```javascript
const token = 'YOUR_ACCESS_TOKEN';
const ws = new WebSocket(`ws://localhost:8000/orders/live?token=${token}`);

ws.onopen = () => {
  console.log('Connected to live orders');
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

ws.onclose = () => {
  console.log('Disconnected from live orders');
};

// Keep connection alive
setInterval(() => {
  if (ws.readyState === WebSocket.OPEN) {
    ws.send('ping');
  }
}, 30000);
```

## Testing with Postman

1. Import the collection by creating a new collection
2. Set environment variable `base_url` = `http://localhost:8000`
3. Set environment variable `token` after login
4. Use `{{base_url}}` and `{{token}}` in requests

## Notes

- Replace `YOUR_ACCESS_TOKEN` with actual token from login response
- Replace IDs (like `/orders/1`) with actual IDs from your database
- For file uploads, ensure the file path is correct
- WebSocket requires a valid JWT token in the query parameter
