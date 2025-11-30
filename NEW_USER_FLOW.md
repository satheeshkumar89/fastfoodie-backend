# 🚀 New User Onboarding Flow

This guide explains the complete flow for a **new restaurant partner** signing up for the first time.

---

## 📋 Flow Overview

1.  **Login** (Verify OTP)
2.  **Create Restaurant** (Setup basic details)
3.  **Add Address** (Set location)
4.  **Add Menu Items** (Build menu)
5.  **Go Live** (Open restaurant)

---

## 🛠️ Step-by-Step Implementation

### 1️⃣ Login & Get Token

**Endpoint:** `POST /auth/verify-otp`

```bash
curl -X POST http://localhost:8000/auth/verify-otp \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+453204589840", "otp_code": "123456"}'
```

**Response:**
```json
{
  "access_token": "eyJhbGci...",
  "owner": {
    "id": 5,
    "email": "temp_+453204589840@fastfoodie.com"
  }
}
```
> **Note:** Save the `access_token` for all subsequent requests.

---

### 2️⃣ Create Restaurant Profile

**Endpoint:** `POST /restaurant/details`

```bash
curl -X POST http://localhost:8000/restaurant/details \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "restaurant_name": "Tasty Bites",
    "restaurant_type": "restaurant",
    "fssai_license_number": "99999999999999",
    "opening_time": "09:00",
    "closing_time": "22:00"
  }'
```

---

### 3️⃣ Add Restaurant Address

**Endpoint:** `POST /restaurant/address`

```bash
curl -X POST http://localhost:8000/restaurant/address \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 12.9716,
    "longitude": 77.5946,
    "address_line_1": "123 New Street",
    "city": "Bangalore",
    "state": "Karnataka",
    "pincode": "560001"
  }'
```

---

### 4️⃣ Add Menu Items

**Endpoint:** `POST /menu/item/add`

```bash
curl -X POST http://localhost:8000/menu/item/add \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Cheese Burger",
    "description": "Juicy burger with extra cheese",
    "price": 199.00,
    "category_id": 4,
    "is_vegetarian": false,
    "preparation_time": 15
  }'
```

---

### 5️⃣ Go Live (Open Restaurant)

**Endpoint:** `PUT /restaurant/status?is_open=true`

```bash
curl -X PUT "http://localhost:8000/restaurant/status?is_open=true" \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**
```json
{
  "success": true,
  "message": "Restaurant is now opened",
  "data": { "is_open": true }
}
```

---

## 📱 Flutter Implementation Check

In your Flutter app, you should check if the user has a restaurant after login.

```dart
// After login, check restaurant status
Future<void> checkRestaurantStatus() async {
  try {
    final response = await http.get(
      Uri.parse('$baseUrl/restaurant/details'),
      headers: {'Authorization': 'Bearer $token'},
    );
    
    if (response.statusCode == 200) {
      // Restaurant exists -> Go to Dashboard
      Navigator.pushReplacementNamed(context, '/dashboard');
    } else if (response.statusCode == 404) {
      // Restaurant NOT found -> Go to Create Restaurant Screen
      Navigator.pushReplacementNamed(context, '/create-restaurant');
    }
  } catch (e) {
    print('Error: $e');
  }
}
```

---

## ✅ Checklist for New User

- [x] **Login:** Working (Fixed unique email issue)
- [x] **Create Restaurant:** Working
- [x] **Add Address:** Working
- [x] **Add Menu:** Working
- [x] **Go Live:** Working (Added new endpoint)

Your backend is now fully ready to onboard new users! 🚀
