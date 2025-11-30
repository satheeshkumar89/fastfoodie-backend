# 🔍 Debugging "Something went wrong" Error

## Common Issues & Solutions

### 1. **Check Your API Base URL**

Make sure your Flutter app is pointing to the correct server:

```dart
// ❌ Wrong (if running on emulator)
const baseUrl = 'http://localhost:8000';

// ✅ Correct (for iOS Simulator)
const baseUrl = 'http://127.0.0.1:8000';

// ✅ Correct (for Android Emulator)
const baseUrl = 'http://10.0.2.2:8000';

// ✅ Correct (for Physical Device on same network)
const baseUrl = 'http://192.168.x.x:8000';  // Your Mac's IP
```

---

### 2. **Check Authentication Token**

The error might be due to an expired or invalid token.

**Test your token:**
```bash
# Get a fresh token
curl -X POST "http://localhost:8000/auth/send-otp" \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+453204589838"}'

# Use the OTP from response
curl -X POST "http://localhost:8000/auth/verify-otp" \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+453204589838", "otp_code": "YOUR_OTP"}'
```

---

### 3. **Test Endpoints Directly**

```bash
# Test categories (no auth needed)
curl http://localhost:8000/menu/categories

# Test menu items (needs auth)
TOKEN="your_token_here"
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/menu/items
```

---

### 4. **Check Server Logs**

Look at your terminal where the server is running for error messages.

Common errors:
- `401 Unauthorized` - Token expired or invalid
- `404 Not Found` - Wrong endpoint URL
- `500 Internal Server Error` - Server-side issue

---

### 5. **Common Flutter Issues**

#### Issue: Network Error
```dart
// Add error handling
try {
  final response = await http.get(
    Uri.parse('$baseUrl/menu/items'),
    headers: {'Authorization': 'Bearer $token'},
  );
  
  if (response.statusCode == 200) {
    // Success
  } else {
    print('Error: ${response.statusCode}');
    print('Body: ${response.body}');
  }
} catch (e) {
  print('Network error: $e');
}
```

#### Issue: Token Not Included
```dart
// Make sure token is in headers
final headers = {
  'Authorization': 'Bearer $token',
  'Content-Type': 'application/json',
};
```

---

### 6. **Get Your Mac's IP Address**

If testing on a physical device:

```bash
# On Mac
ipconfig getifaddr en0
```

Then use this IP in your Flutter app:
```dart
const baseUrl = 'http://YOUR_MAC_IP:8000';
```

---

### 7. **Test with Postman First**

Before testing in Flutter:
1. Open Postman
2. Test `GET http://localhost:8000/menu/categories`
3. Test `POST http://localhost:8000/auth/send-otp`
4. If these work, the issue is in your Flutter app

---

### 8. **Enable Detailed Logging in Flutter**

```dart
import 'package:http/http.dart' as http;

Future<void> fetchMenuItems() async {
  try {
    print('📡 Calling: $baseUrl/menu/items');
    print('🔑 Token: ${token.substring(0, 20)}...');
    
    final response = await http.get(
      Uri.parse('$baseUrl/menu/items'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
    );
    
    print('📊 Status Code: ${response.statusCode}');
    print('📦 Response Body: ${response.body}');
    
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      print('✅ Success: ${data['message']}');
    } else {
      print('❌ Error: ${response.statusCode}');
      print('Details: ${response.body}');
    }
  } catch (e, stackTrace) {
    print('❌ Exception: $e');
    print('Stack trace: $stackTrace');
  }
}
```

---

### 9. **Quick Test Script**

Save this as `test_connection.dart`:

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() async {
  // Test 1: Server health
  print('🧪 Test 1: Server Health');
  try {
    final response = await http.get(Uri.parse('http://127.0.0.1:8000/'));
    print('✅ Server is running: ${response.body}');
  } catch (e) {
    print('❌ Cannot connect to server: $e');
    return;
  }
  
  // Test 2: Categories
  print('\n🧪 Test 2: Get Categories');
  try {
    final response = await http.get(
      Uri.parse('http://127.0.0.1:8000/menu/categories')
    );
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      print('✅ Got ${data['data']['categories'].length} categories');
    }
  } catch (e) {
    print('❌ Error: $e');
  }
  
  // Test 3: Send OTP
  print('\n🧪 Test 3: Send OTP');
  try {
    final response = await http.post(
      Uri.parse('http://127.0.0.1:8000/auth/send-otp'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({'phone_number': '+453204589838'}),
    );
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      print('✅ OTP sent: ${data['data']['otp']}');
    }
  } catch (e) {
    print('❌ Error: $e');
  }
}
```

Run it:
```bash
dart test_connection.dart
```

---

### 10. **Check These Common Mistakes**

- [ ] Server is running on port 8000
- [ ] Using correct IP address for your device
- [ ] Token is not expired
- [ ] Token is included in Authorization header
- [ ] Content-Type header is set
- [ ] Request body is properly JSON encoded
- [ ] No typos in endpoint URLs

---

## 🆘 Still Not Working?

### Share These Details:

1. **Server Status:**
```bash
curl http://localhost:8000/
```

2. **Which endpoint is failing?**
   - Login?
   - Menu items?
   - Categories?

3. **Flutter Console Output:**
   - Any error messages?
   - Network errors?

4. **Testing Device:**
   - iOS Simulator?
   - Android Emulator?
   - Physical device?

5. **Server Logs:**
   - Check terminal where server is running
   - Look for error messages

---

## ✅ Quick Fix Checklist

```dart
// 1. Correct base URL
const baseUrl = 'http://127.0.0.1:8000';  // For iOS Simulator

// 2. Include token
final headers = {
  'Authorization': 'Bearer $token',
  'Content-Type': 'application/json',
};

// 3. Handle errors
try {
  final response = await http.get(url, headers: headers);
  if (response.statusCode == 200) {
    // Success
  } else {
    print('Error: ${response.statusCode} - ${response.body}');
  }
} catch (e) {
  print('Network error: $e');
}

// 4. Check token expiry
// Tokens expire after 30 days - get a new one if needed
```

---

**Need more help?** Share:
- The specific screen that's failing
- Console output from Flutter
- Server logs from terminal
