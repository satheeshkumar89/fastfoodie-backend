# 🏪 Restaurant Status API - Dashboard Header

## 📱 Overview

New API endpoints for the dashboard header showing:
- Restaurant name
- Online/Offline status toggle
- Location (latitude/longitude)
- Opening hours

---

## 🎯 New Endpoints

### 1. Get Restaurant Status
**Endpoint:** `GET /dashboard/restaurant-status`

**Purpose:** Get restaurant info for dashboard header

**Response:**
```json
{
  "success": true,
  "message": "Restaurant status retrieved successfully",
  "data": {
    "restaurant_id": 1,
    "restaurant_name": "Tasty Bites",
    "is_open": true,
    "location": {
      "latitude": 12.9716,
      "longitude": 77.5946,
      "address": "123 Main Street",
      "city": "Bangalore"
    },
    "opening_time": "09:00",
    "closing_time": "22:00",
    "verification_status": "approved"
  }
}
```

### 2. Toggle Online/Offline Status
**Endpoint:** `PUT /dashboard/toggle-status`

**Purpose:** Toggle restaurant between online and offline

**Request:** No body needed (just PUT request)

**Response:**
```json
{
  "success": true,
  "message": "Restaurant is now online",
  "data": {
    "restaurant_id": 1,
    "restaurant_name": "Tasty Bites",
    "is_open": true,
    "status": "online"
  }
}
```

---

## 📱 UI Implementation

### Dashboard Header Component

```dart
// Flutter Example
class DashboardHeader extends StatefulWidget {
  @override
  _DashboardHeaderState createState() => _DashboardHeaderState();
}

class _DashboardHeaderState extends State<DashboardHeader> {
  bool isOnline = false;
  String restaurantName = "";
  Map<String, dynamic>? location;

  @override
  void initState() {
    super.initState();
    loadRestaurantStatus();
  }

  Future<void> loadRestaurantStatus() async {
    final response = await api.get('/dashboard/restaurant-status');
    setState(() {
      restaurantName = response['data']['restaurant_name'];
      isOnline = response['data']['is_open'];
      location = response['data']['location'];
    });
  }

  Future<void> toggleStatus() async {
    final response = await api.put('/dashboard/toggle-status');
    setState(() {
      isOnline = response['data']['is_open'];
    });
    
    // Show snackbar
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(response['message']))
    );
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.all(16),
      child: Row(
        children: [
          // Back button
          IconButton(
            icon: Icon(Icons.arrow_back),
            onPressed: () => Navigator.pop(context),
          ),
          
          // Restaurant name
          Expanded(
            child: Text(
              restaurantName,
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
          
          // Online/Offline indicator
          Container(
            padding: EdgeInsets.symmetric(horizontal: 12, vertical: 6),
            decoration: BoxDecoration(
              color: isOnline ? Colors.green.shade50 : Colors.red.shade50,
              borderRadius: BorderRadius.circular(20),
            ),
            child: Row(
              children: [
                Container(
                  width: 8,
                  height: 8,
                  decoration: BoxDecoration(
                    color: isOnline ? Colors.green : Colors.red,
                    shape: BoxShape.circle,
                  ),
                ),
                SizedBox(width: 6),
                Text(
                  isOnline ? 'Online' : 'Offline',
                  style: TextStyle(
                    color: isOnline ? Colors.green : Colors.red,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ],
            ),
          ),
          
          SizedBox(width: 12),
          
          // Toggle switch
          Switch(
            value: isOnline,
            onChanged: (value) => toggleStatus(),
            activeColor: Colors.green,
          ),
        ],
      ),
    );
  }
}
```

---

## 🎨 UI Design (Based on Screenshot)

```
┌─────────────────────────────────────────────┐
│  ←  RestaurantPa...  ● Online  [Toggle]    │
└─────────────────────────────────────────────┘
```

### Elements:
1. **Back Arrow** - Navigate back
2. **Restaurant Name** - Truncated if too long
3. **Status Indicator** - Green dot + "Online" text
4. **Toggle Switch** - Turn on/off

---

## 🔄 Complete Flow

### 1. Load Dashboard
```
GET /dashboard/restaurant-status
↓
Display: Restaurant name, status, location
```

### 2. User Toggles Switch
```
PUT /dashboard/toggle-status
↓
Update UI with new status
↓
Show success message
```

### 3. Location Usage
```
Use latitude/longitude for:
- Showing on map
- Distance calculations
- Delivery radius
```

---

## 📊 Response Fields Explained

| Field | Type | Description |
|-------|------|-------------|
| `restaurant_id` | integer | Unique restaurant ID |
| `restaurant_name` | string | Restaurant name |
| `is_open` | boolean | true = online, false = offline |
| `location.latitude` | float | GPS latitude |
| `location.longitude` | float | GPS longitude |
| `location.address` | string | Street address |
| `location.city` | string | City name |
| `opening_time` | string | Opening time (HH:MM) |
| `closing_time` | string | Closing time (HH:MM) |
| `verification_status` | string | KYC status |

---

## 🎯 Use Cases

### Use Case 1: Restaurant Goes Offline for Break
```
1. Owner toggles switch OFF
2. PUT /dashboard/toggle-status
3. is_open = false
4. Customers can't place new orders
```

### Use Case 2: Restaurant Opens for Day
```
1. Owner toggles switch ON
2. PUT /dashboard/toggle-status
3. is_open = true
4. Restaurant appears in customer app
```

### Use Case 3: Show on Map
```
1. GET /dashboard/restaurant-status
2. Extract latitude/longitude
3. Display restaurant location on map
4. Show delivery radius
```

---

## 🔐 Security

- ✅ Requires authentication (Bearer token)
- ✅ Only restaurant owner can toggle status
- ✅ Uses `get_current_restaurant` dependency

---

## 🧪 Testing

### Test 1: Get Status
```bash
curl -X GET "http://localhost:8000/dashboard/restaurant-status" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Test 2: Toggle Status
```bash
curl -X PUT "http://localhost:8000/dashboard/toggle-status" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Test 3: Toggle Again (should reverse)
```bash
curl -X PUT "http://localhost:8000/dashboard/toggle-status" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 📱 React/React Native Example

```javascript
import React, { useState, useEffect } from 'react';

const DashboardHeader = () => {
  const [restaurantData, setRestaurantData] = useState(null);
  const [isOnline, setIsOnline] = useState(false);

  useEffect(() => {
    loadStatus();
  }, []);

  const loadStatus = async () => {
    const response = await fetch('/dashboard/restaurant-status', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const data = await response.json();
    setRestaurantData(data.data);
    setIsOnline(data.data.is_open);
  };

  const toggleStatus = async () => {
    const response = await fetch('/dashboard/toggle-status', {
      method: 'PUT',
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const data = await response.json();
    setIsOnline(data.data.is_open);
    alert(data.message);
  };

  return (
    <div className="dashboard-header">
      <button onClick={() => history.back()}>←</button>
      
      <h2>{restaurantData?.restaurant_name}</h2>
      
      <div className={`status ${isOnline ? 'online' : 'offline'}`}>
        <span className="dot"></span>
        {isOnline ? 'Online' : 'Offline'}
      </div>
      
      <label className="switch">
        <input 
          type="checkbox" 
          checked={isOnline}
          onChange={toggleStatus}
        />
        <span className="slider"></span>
      </label>
    </div>
  );
};
```

---

## ✅ Summary

### New Endpoints:
1. `GET /dashboard/restaurant-status` - Get status & location
2. `PUT /dashboard/toggle-status` - Toggle online/offline

### Data Returned:
- Restaurant name
- Online/Offline status
- Location (lat/long)
- Opening hours
- Verification status

### Perfect For:
- Dashboard header
- Status toggle switch
- Location-based features
- Business hours display

**Your dashboard header API is ready!** 🎉
