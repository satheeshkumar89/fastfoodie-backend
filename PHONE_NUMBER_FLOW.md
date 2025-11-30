# Phone Number Flow - New vs Existing User Detection

This document explains how to determine whether a phone number is **new** (first-time user) or **existing** (returning user) after the `verify-otp` API call.

## 📋 Table of Contents
1. [Overview](#overview)
2. [Authentication Flow](#authentication-flow)
3. [How to Detect New vs Existing User](#how-to-detect-new-vs-existing-user)
4. [API Response Structure](#api-response-structure)
5. [Implementation Examples](#implementation-examples)
6. [Complete Flow Diagram](#complete-flow-diagram)

---

## Overview

The FastFoodie backend uses a **phone-based authentication system** with OTP verification. After successful OTP verification, the system needs to determine if the user is:
- **New User**: Phone number not registered before (needs onboarding)
- **Existing User**: Phone number already registered (direct access to dashboard)

---

## Authentication Flow

### Step 1: Send OTP
```bash
POST /auth/send-otp
{
  "phone_number": "+919876543210"
}
```

**Backend Logic:**
1. Checks if an `Owner` record exists with this phone number
2. Creates an OTP record (linked to owner_id if exists, null if new)
3. Sends OTP via SMS
4. Returns success response

### Step 2: Verify OTP
```bash
POST /auth/verify-otp
{
  "phone_number": "+919876543210",
  "otp_code": "123456"
}
```

**Backend Logic** (from `app/routers/auth.py`):
```python
# 1. Verify OTP is valid and not expired
is_valid = verify_otp(db, request.phone_number, request.otp_code)

# 2. Check if owner exists
owner = db.query(Owner).filter(Owner.phone_number == request.phone_number).first()

# 3. If owner doesn't exist, create new owner with minimal info
if not owner:
    owner = Owner(
        phone_number=request.phone_number,
        full_name="",  # Empty - needs to be filled
        email=""       # Empty - needs to be filled
    )
    db.add(owner)
    db.commit()

# 4. Create JWT token
access_token = create_access_token(
    data={"owner_id": owner.id, "phone_number": owner.phone_number}
)

# 5. Return token with owner details
return TokenResponse(
    access_token=access_token,
    token_type="bearer",
    owner=OwnerResponse.from_orm(owner)
)
```

---

## How to Detect New vs Existing User

### Method 1: Check `full_name` and `email` Fields ✅ **RECOMMENDED**

After receiving the `verify-otp` response, check the `owner` object:

```javascript
// Response from verify-otp
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "owner": {
    "id": 123,
    "full_name": "",        // ← Check this
    "email": "",            // ← Check this
    "phone_number": "+919876543210",
    "is_active": true,
    "created_at": "2025-11-25T15:30:00Z"
  }
}
```

**Detection Logic:**
```javascript
function isNewUser(ownerData) {
  // New user if full_name OR email is empty
  return !ownerData.full_name || !ownerData.email || 
         ownerData.full_name === "" || ownerData.email === "";
}

// Usage
const response = await verifyOTP(phoneNumber, otpCode);
if (isNewUser(response.owner)) {
  // Navigate to: Create Owner Details screen
  navigateTo('/owner/create-details');
} else {
  // Navigate to: Dashboard (existing user)
  navigateTo('/dashboard');
}
```

### Method 2: Check `created_at` Timestamp

Compare the `created_at` timestamp with the current time:

```javascript
function isNewUser(ownerData) {
  const createdAt = new Date(ownerData.created_at);
  const now = new Date();
  const diffInSeconds = (now - createdAt) / 1000;
  
  // If account created within last 10 seconds, it's a new user
  return diffInSeconds < 10;
}
```

⚠️ **Note**: This method is less reliable due to potential time sync issues.

### Method 3: Check Restaurant Existence (Most Comprehensive)

For the most accurate detection, check if the user has completed onboarding:

```javascript
async function getUserOnboardingStatus(accessToken) {
  try {
    // Try to get restaurant details
    const response = await fetch('/restaurant/verification-status', {
      headers: { 'Authorization': `Bearer ${accessToken}` }
    });
    
    if (response.status === 404) {
      return 'NEW_USER'; // No restaurant setup
    }
    
    const data = await response.json();
    
    // Check owner details
    if (!data.owner.full_name || !data.owner.email) {
      return 'INCOMPLETE_PROFILE'; // Started but not completed
    }
    
    return 'EXISTING_USER'; // Fully onboarded
    
  } catch (error) {
    return 'NEW_USER'; // Default to new user
  }
}
```

---

## API Response Structure

### Verify OTP Response

```typescript
interface TokenResponse {
  access_token: string;      // JWT token for authentication
  token_type: string;        // Always "bearer"
  owner: OwnerResponse;      // Owner details
}

interface OwnerResponse {
  id: number;                // Owner ID
  full_name: string;         // Empty "" for new users
  email: string;             // Empty "" for new users
  phone_number: string;      // Verified phone number
  is_active: boolean;        // Always true
  created_at: string;        // ISO 8601 timestamp
}
```

### Example Responses

**New User (First Time):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "owner": {
    "id": 42,
    "full_name": "",
    "email": "",
    "phone_number": "+919876543210",
    "is_active": true,
    "created_at": "2025-11-25T15:30:45.123Z"
  }
}
```

**Existing User (Returning):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "owner": {
    "id": 42,
    "full_name": "John Doe",
    "email": "john@example.com",
    "phone_number": "+919876543210",
    "is_active": true,
    "created_at": "2025-11-20T10:15:30.456Z"
  }
}
```

---

## Implementation Examples

### Flutter/Dart Example

```dart
class AuthService {
  Future<void> handleOTPVerification(String phoneNumber, String otp) async {
    final response = await verifyOTP(phoneNumber, otp);
    
    // Store token
    await storage.write(key: 'access_token', value: response.accessToken);
    
    // Check if new user
    if (isNewUser(response.owner)) {
      // New user - navigate to onboarding
      Get.offAll(() => CreateOwnerDetailsScreen());
    } else {
      // Existing user - navigate to dashboard
      Get.offAll(() => DashboardScreen());
    }
  }
  
  bool isNewUser(OwnerResponse owner) {
    return owner.fullName.isEmpty || owner.email.isEmpty;
  }
}
```

### JavaScript/React Example

```javascript
const handleVerifyOTP = async (phoneNumber, otpCode) => {
  try {
    const response = await fetch('/auth/verify-otp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ phone_number: phoneNumber, otp_code: otpCode })
    });
    
    const data = await response.json();
    
    // Store token
    localStorage.setItem('access_token', data.access_token);
    
    // Check user status
    if (!data.owner.full_name || !data.owner.email) {
      // New user - redirect to profile setup
      navigate('/onboarding/profile-setup');
    } else {
      // Existing user - redirect to dashboard
      navigate('/dashboard');
    }
    
  } catch (error) {
    console.error('OTP verification failed:', error);
  }
};
```

### Python Example

```python
import requests

def handle_otp_verification(phone_number: str, otp_code: str):
    response = requests.post(
        'http://localhost:8000/auth/verify-otp',
        json={'phone_number': phone_number, 'otp_code': otp_code}
    )
    
    data = response.json()
    
    # Store token
    access_token = data['access_token']
    
    # Check if new user
    owner = data['owner']
    is_new = not owner['full_name'] or not owner['email']
    
    if is_new:
        print("New user - show onboarding")
        return 'ONBOARDING'
    else:
        print("Existing user - show dashboard")
        return 'DASHBOARD'
```

---

## Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    USER ENTERS PHONE NUMBER                  │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    POST /auth/send-otp                       │
│                 { phone_number: "+91..." }                   │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Backend checks if Owner exists                  │
│         Creates OTP (linked to owner_id or null)             │
│                    Sends SMS with OTP                        │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    USER ENTERS OTP CODE                      │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   POST /auth/verify-otp                      │
│         { phone_number: "+91...", otp_code: "123456" }       │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Backend verifies OTP is valid                   │
└───────────────────────────┬─────────────────────────────────┘
                            │
                ┌───────────┴───────────┐
                │                       │
                ▼                       ▼
    ┌───────────────────┐   ┌───────────────────┐
    │  Owner EXISTS?    │   │  Owner NOT FOUND  │
    │  (Existing User)  │   │   (New User)      │
    └─────────┬─────────┘   └─────────┬─────────┘
              │                       │
              │                       ▼
              │           ┌───────────────────────┐
              │           │  Create new Owner:    │
              │           │  - phone_number: set  │
              │           │  - full_name: ""      │
              │           │  - email: ""          │
              │           └───────────┬───────────┘
              │                       │
              └───────────┬───────────┘
                          │
                          ▼
        ┌─────────────────────────────────────┐
        │   Generate JWT Token with:          │
        │   - owner_id                        │
        │   - phone_number                    │
        └─────────────────┬───────────────────┘
                          │
                          ▼
        ┌─────────────────────────────────────┐
        │   Return TokenResponse:             │
        │   - access_token                    │
        │   - token_type: "bearer"            │
        │   - owner: { id, full_name, email,  │
        │              phone_number, ... }    │
        └─────────────────┬───────────────────┘
                          │
                          ▼
        ┌─────────────────────────────────────┐
        │   CLIENT CHECKS OWNER DATA:         │
        │                                     │
        │   if (full_name == "" || email == "")│
        └─────────────────┬───────────────────┘
                          │
              ┌───────────┴───────────┐
              │                       │
              ▼                       ▼
    ┌─────────────────┐   ┌─────────────────────┐
    │   NEW USER      │   │   EXISTING USER     │
    │                 │   │                     │
    │ Navigate to:    │   │ Navigate to:        │
    │ - Create Owner  │   │ - Dashboard         │
    │   Details       │   │ - Home Screen       │
    │ - Onboarding    │   │                     │
    └─────────────────┘   └─────────────────────┘
```

---

## Summary

### ✅ Best Practice: Check `full_name` and `email`

```javascript
// RECOMMENDED APPROACH
const isNewUser = !owner.full_name || !owner.email;

if (isNewUser) {
  // Show: Create Owner Details screen
  // Next: POST /owner/details
} else {
  // Show: Dashboard
  // User is fully onboarded
}
```

### 📝 Key Points

1. **New users** have empty `full_name` and `email` fields
2. **Existing users** have populated `full_name` and `email` fields
3. Both new and existing users receive a valid JWT token
4. The `created_at` field shows when the account was created
5. New users must complete the onboarding flow:
   - Create Owner Details (`POST /owner/details`)
   - Create Restaurant Details (`POST /restaurant/details`)
   - Add Cuisines, Address, Documents, etc.

### 🔄 Next Steps After Detection

**For New Users:**
1. Navigate to "Create Owner Details" screen
2. Collect: `full_name`, `email`, `phone_number`
3. Submit: `POST /owner/details`
4. Continue with restaurant setup

**For Existing Users:**
1. Navigate to Dashboard
2. Load user's restaurant data
3. Show orders, menu, analytics, etc.

---

## Related Documentation

- [API Testing Guide](./API_TESTING.md) - Complete API examples
- [Authentication Flow](./app/routers/auth.py) - Backend implementation
- [Database Models](./app/models.py) - Owner and Restaurant models
- [Schemas](./app/schemas.py) - Request/Response structures
