# 📍 REAL-TIME LOCATION TRACKING SYSTEM

## Complete Guide for Customer & Delivery Partner Location Tracking

---

## 🎯 OVERVIEW

The location tracking system enables **real-time tracking** of delivery partners during active deliveries, allowing customers to see exactly where their order is and get accurate ETAs.

### Key Features:
- ✅ **Real-time GPS tracking** - Updated every 5-10 seconds
- ✅ **Delivery partner location** - Latitude, longitude, speed, bearing
- ✅ **Customer tracking** - See delivery partner on map
- ✅ **ETA calculation** - Estimated time of arrival
- ✅ **Location history** - Full tracking history for analytics
- ✅ **Privacy-focused** - Location only shared during active deliveries

---

## 🚀 HOW IT WORKS

### For Delivery Partners:
```
1. Partner accepts order
2. Partner starts delivery (status: picked_up)
3. App sends GPS location every 5-10 seconds
4. Location stored with timestamp, speed, bearing
5. Location tracking stops when order delivered
```

### For Customers:
```
1. Customer places order
2. Order gets assigned to delivery partner
3. Customer opens "Track Order" screen
4. Map shows delivery partner's real-time location
5. ETA updates dynamically based on partner's speed
```

---

## 📡 API ENDPOINTS

### 1. **Delivery Partner: Update Location**
**Endpoint:** `POST /delivery-partner/location/update`
**Auth:** Required (Delivery Partner)

**Description:** Delivery partner sends their current GPS location. Should be called every 5-10 seconds during active delivery.

**Request Body:**
```json
{
  "latitude": 12.9716,
  "longitude": 77.5946,
  "accuracy": 10.5,
  "bearing": 45.0,
  "speed": 8.33,
  "order_id": 123
}
```

**Field Descriptions:**
- `latitude` - GPS latitude (-90 to 90)
- `longitude` - GPS longitude (-180 to 180)
- `accuracy` - GPS accuracy in meters (optional)
- `bearing` - Direction of movement 0-360 degrees (optional)
- `speed` - Speed in meters per second (optional)
- `order_id` - Currently delivering this order (optional)

**Response:**
```json
{
  "success": true,
  "message": "Location updated successfully",
  "data": {
    "latitude": 12.9716,
    "longitude": 77.5946,
    "timestamp": "2024-12-24T13:30:45Z"
  }
}
```

---

### 2. **Delivery Partner: Get Current Location**
**Endpoint:** `GET /delivery-partner/location/current`
**Auth:** Required (Delivery Partner)

**Description:** Get delivery partner's most recent location.

**Response:**
```json
{
  "success": true,
  "message": "Location retrieved successfully",
  "data": {
    "latitude": 12.9716,
    "longitude": 77.5946,
    "accuracy": 10.5,
    "bearing": 45.0,
    "speed": 8.33,
    "updated_at": "2024-12-24T13:30:45Z"
  }
}
```

---

### 3. **Customer: Track Delivery Partner**
**Endpoint:** `GET /customer/orders/{order_id}/track-location`
**Auth:** Required (Customer)

**Description:** Track delivery partner's real-time location for an active order.

**Response (When tracking available):**
```json
{
  "success": true,
  "message": "Delivery partner location retrieved",
  "data": {
    "tracking_available": true,
    "delivery_partner": {
      "id": 2,
      "name": "Amit Sharma",
      "phone": "+919999888877",
      "vehicle_type": "scooter",
      "vehicle_number": "DL01XY9876",
      "rating": 5.0
    },
    "location": {
      "latitude": 12.9716,
      "longitude": 77.5946,
      "accuracy": 10.5,
      "bearing": 45.0,
      "speed_mps": 8.33,
      "speed_kmh": 30.0,
      "last_updated": "2024-12-24T13:30:45Z"
    },
    "eta_minutes": 14,
    "order_status": "picked_up"
  }
}
```

**Response (When no partner assigned yet):**
```json
{
  "success": true,
  "message": "No delivery partner assigned yet",
  "data": {
    "tracking_available": false,
    "message": "Delivery partner will be assigned soon"
  }
}
```

---

## 📊 DATABASE SCHEMA

### Table: `delivery_partner_locations`

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| delivery_partner_id | INTEGER | FK to delivery_partners |
| order_id | INTEGER | FK to orders (optional) |
| latitude | REAL | GPS latitude |
| longitude | REAL | GPS longitude |
| accuracy | REAL | GPS accuracy in meters |
| bearing | REAL | Direction 0-360 degrees |
| speed | REAL | Speed in m/s |
| address | TEXT | Reverse geocoded address |
| created_at | TIMESTAMP | When location was recorded |
| updated_at | TIMESTAMP | Last update time |

**Indexes:**
- delivery_partner_id
- order_id  
- created_at (for efficient queries)

---

### Table: `customer_locations`

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| customer_id | INTEGER | FK to customers |
| order_id | INTEGER | FK to orders |
| latitude | REAL | Delivery address latitude |
| longitude | REAL | Delivery address longitude |
| address | TEXT | Full delivery address |
| landmark | TEXT | Nearby landmark |
| created_at | TIMESTAMP | When stored |

---

## 📱 FLUTTER IMPLEMENTATION GUIDE

### Step 1: Setup Location Services

#### Add Dependencies (pubspec.yaml):
```yaml
dependencies:
  google_maps_flutter: ^2.5.0
  geolocator: ^10.1.0
  permission_handler: ^11.0.1
```

#### Request Location Permission:
```dart
Future<bool> requestLocationPermission() async {
  LocationPermission permission = await Geolocator.checkPermission();
  
  if (permission == LocationPermission.denied) {
    permission = await Geolocator.requestPermission();
  }
  
  return permission == LocationPermission.whileInUse || 
         permission == LocationPermission.always;
}
```

---

### Step 2: Delivery Partner - Send Location

```dart
class LocationTrackingService {
  Timer? _locationTimer;
  final DeliveryPartnerRepository repository;
  
  void startTracking(int orderId) {
    _locationTimer = Timer.periodic(Duration(seconds: 10), (timer) async {
      Position position = await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high,
      );
      
      await repository.updateLocation(
        latitude: position.latitude,
        longitude: position.longitude,
        accuracy: position.accuracy,
        bearing: position.heading,
        speed: position.speed,
        orderId: orderId,
      );
    });
  }
  
  void stopTracking() {
    _locationTimer?.cancel();
    _locationTimer = null;
  }
}
```

#### Repository Method:
```dart
Future<void> updateLocation({
  required double latitude,
  required double longitude,
  double? accuracy,
  double? bearing,
  double? speed,
  int? orderId,
}) async {
  final response = await http.post(
    Uri.parse('$baseUrl/delivery-partner/location/update'),
    headers: {
      'Authorization': 'Bearer $token',
      'Content-Type': 'application/json',
    },
    body: jsonEncode({
      'latitude': latitude,
      'longitude': longitude,
      'accuracy': accuracy,
      'bearing': bearing,
      'speed': speed,
      'order_id': orderId,
    }),
  );
  
  if (response.statusCode != 200) {
    throw Exception('Failed to update location');
  }
}
```

---

### Step 3: Customer - Track Delivery Partner

```dart
class OrderTrackingScreen extends StatefulWidget {
  final int orderId;
  
  @override
  _OrderTrackingScreenState createState() => _OrderTrackingScreenState();
}

class _OrderTrackingScreenState extends State<OrderTrackingScreen> {
  GoogleMapController? mapController;
  Timer? _trackingTimer;
  LatLng? deliveryPartnerLocation;
  
  @override
  void initState() {
    super.initState();
    _startTracking();
  }
  
  void _startTracking() {
    _trackingTimer = Timer.periodic(Duration(seconds: 5), (timer) {
      _fetchDeliveryPartnerLocation();
    });
    _fetchDeliveryPartnerLocation(); // Initial fetch
  }
  
  Future<void> _fetchDeliveryPartnerLocation() async {
    final response = await http.get(
      Uri.parse('$baseUrl/customer/orders/${widget.orderId}/track-location'),
      headers: {'Authorization': 'Bearer $token'},
    );
    
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      
      if (data['data']['tracking_available']) {
        setState(() {
          deliveryPartnerLocation = LatLng(
            data['data']['location']['latitude'],
            data['data']['location']['longitude'],
          );
        });
        
        // Move camera to delivery partner location
        mapController?.animateCamera(
          CameraUpdate.newLatLng(deliveryPartnerLocation!),
        );
      }
    }
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: GoogleMap(
        initialCameraPosition: CameraPosition(
          target: deliveryPartnerLocation ?? LatLng(12.9716, 77.5946),
          zoom: 15,
        ),
        markers: {
          if (deliveryPartnerLocation != null)
            Marker(
              markerId: MarkerId('delivery_partner'),
              position: deliveryPartnerLocation!,
              icon: BitmapDescriptor.defaultMarkerWithHue(
                BitmapDescriptor.hueGreen
              ),
              infoWindow: InfoWindow(title: 'Delivery Partner'),
            ),
        },
        onMapCreated: (controller) {
          mapController = controller;
        },
      ),
    );
  }
  
  @override
  void dispose() {
    _trackingTimer?.cancel();
    super.dispose();
  }
}
```

---

## ⚙️ RECOMMENDED SETTINGS

### Location Update Frequency:

| Scenario | Update Interval | Reason |
|----------|----------------|--------|
| Active Delivery | 5-10 seconds | Real-time tracking |
| Partner Online (idle) | 30 seconds | Battery saving |
| Partner Offline | Stop updates | Privacy & battery |

### GPS Accuracy:
- **Delivery Partner App:** `HIGH` accuracy (< 10 meters)
- **Customer App:** Not needed (only displaying location)

### Battery Optimization:
```dart
// Use location accuracy based on speed
LocationAccuracy getAccuracy(double speed) {
  if (speed > 5) return LocationAccuracy.high;  // Moving fast
  if (speed > 1) return LocationAccuracy.medium; // Moving slow
  return LocationAccuracy.low; // Stationary
}
```

---

## 🔒 PRIVACY & SECURITY

### Privacy Measures:
1. ✅ **Location shared only during active deliveries**
2. ✅ **Customer can only see their delivery partner**
3. ✅ **Location data auto-deleted after 30 days**
4. ✅ **No location sharing when partner is offline**

### Security:
```
1. JWT token required for all endpoints
2. Customer can only track their own orders
3. Delivery partner can only update their own location
4. Order ID verification before location sharing
```

---

## 📈 ANALYTICS & INSIGHTS

### Useful Queries:

**1. Average Delivery Speed:**
```sql
SELECT AVG(speed) * 3.6 as avg_speed_kmh
FROM delivery_partner_locations
WHERE delivery_partner_id = ?
AND order_id IS NOT NULL;
```

**2. Delivery Route History:**
```sql
SELECT latitude, longitude, created_at
FROM delivery_partner_locations
WHERE order_id = ?
ORDER BY created_at ASC;
```

**3. Partner Activity Heatmap:**
```sql
SELECT latitude, longitude, COUNT(*) as visit_count
FROM delivery_partner_locations
WHERE delivery_partner_id = ?
GROUP BY ROUND(latitude, 3), ROUND(longitude, 3)
HAVING visit_count > 5;
```

---

## 🧪 TESTING GUIDE

### Test Delivery Partner Location Update:
```bash
TOKEN="your_delivery_partner_token"

curl -X POST "http://localhost:8000/delivery-partner/location/update" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 12.9716,
    "longitude": 77.5946,
    "accuracy": 10.5,
    "bearing": 45.0,
    "speed": 8.33,
    "order_id": 1
  }'
```

### Test Customer Tracking:
```bash
TOKEN="your_customer_token"

curl -X GET "http://localhost:8000/customer/orders/1/track-location" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🎯 BEST PRACTICES

### 1. **Efficient Location Updates**
```dart
// Only send location if it has changed significantly
Position? lastPosition;
const double MIN_DISTANCE_METERS = 10;

if (lastPosition != null) {
  double distance = Geolocator.distanceBetween(
    lastPosition!.latitude,
    lastPosition!.longitude,
    newPosition.latitude,
    newPosition.longitude,
  );
  
  if (distance < MIN_DISTANCE_METERS) {
    return; // Skip update
  }
}

lastPosition = newPosition;
await updateLocation(newPosition);
```

### 2. **Handle Network Failures**
```dart
// Queue locations if offline, sync when online
List<LocationUpdate> pendingUpdates = [];

try {
  await updateLocation(position);
} catch (e) {
  pendingUpdates.add(LocationUpdate(position));
}

// Sync when online
if (isOnline && pendingUpdates.isNotEmpty) {
  for (var update in pendingUpdates) {
    await updateLocation(update.position);
  }
  pendingUpdates.clear();
}
```

### 3. **Battery Optimization**
```dart
// Stop tracking when app in background (optional)
@override
void didChangeAppLifecycleState(AppLifecycleState state) {
  if (state == AppLifecycleState.paused) {
    locationService.stopTracking();
  } else if (state == AppLifecycleState.resumed) {
    locationService.startTracking(currentOrderId);
  }
}
```

---

## 🎨 UI/UX RECOMMENDATIONS

### Customer Tracking Screen:
```
┌────────────────────────────────────┐
│     Track Your Order               │
├────────────────────────────────────┤
│                                    │
│    [     Google Map View      ]   │
│    [  🚴 Delivery Partner Marker] │
│    [  📍 Delivery Location     ]   │
│                                    │
├────────────────────────────────────┤
│  🚴 Amit Sharma                    │
│  Scooter • DL01XY9876              │
│  ⭐ 5.0 • 14 min away              │
│                                    │
│  📞 [Call]    💬 [Chat]            │
└────────────────────────────────────┘
```

---

## ✅ SUMMARY

**What's Implemented:**
- ✅ Delivery partner location update API
- ✅ Customer location tracking API
- ✅ Database tables for location storage
- ✅ GPS accuracy, bearing, speed tracking
- ✅ ETA calculation
- ✅ Privacy controls
- ✅ Complete Flutter integration guide

**Total New Endpoints: 3**
- `POST /delivery-partner/location/update`
- `GET /delivery-partner/location/current`
- `GET /customer/orders/{id}/track-location`

---

**Status:** ✅ Production Ready  
**Last Updated:** December 24, 2024  
**Feature:** Real-time Location Tracking System
