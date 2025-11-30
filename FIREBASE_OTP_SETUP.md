# Firebase OTP Authentication Setup

## Overview
The FastFoodie backend uses Firebase Authentication for OTP-based phone number verification. The system works in two modes:

### Development Mode (Default)
- No Firebase configuration required
- OTP is printed to the console
- Perfect for testing and development

### Production Mode (Firebase Enabled)
- Real SMS OTP delivery via Firebase
- Secure token-based authentication
- Production-ready

## How It Works

### 1. Send OTP Flow
```
POST /auth/send-otp
{
  "phone_number": "+919876543210"
}
```

**Development Mode Response:**
- OTP is printed in the terminal
- Returns success message
- OTP is stored in database for verification

**Production Mode:**
- Firebase sends real SMS to the phone number
- Returns session info

### 2. Verify OTP Flow
```
POST /auth/verify-otp
{
  "phone_number": "+919876543210",
  "otp_code": "123456"
}
```

**Response:**
- Returns JWT access token
- Creates or retrieves user account
- Token used for all authenticated endpoints

## Setup for Production (Firebase)

### Step 1: Create Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or select existing one
3. Enable **Authentication** → **Phone** sign-in method

### Step 2: Get Service Account Key
1. Go to **Project Settings** → **Service Accounts**
2. Click **Generate New Private Key**
3. Save the JSON file as `firebase-service-account.json`
4. Place it in the project root directory

### Step 3: Configure Environment
Add to your `.env` file:
```bash
FIREBASE_SERVICE_ACCOUNT_KEY=firebase-service-account.json
```

### Step 4: Restart Server
The Firebase SDK will automatically initialize on startup.

## Testing in Development Mode

### Using Swagger UI (http://localhost:8000/docs)

1. **Send OTP:**
   - Navigate to `/auth/send-otp`
   - Click "Try it out"
   - Enter phone number: `+919876543210`
   - Execute
   - Check terminal for OTP code

2. **Verify OTP:**
   - Navigate to `/auth/verify-otp`
   - Enter the phone number and OTP from terminal
   - Execute
   - Copy the `access_token` from response

3. **Use Authenticated Endpoints:**
   - Click "Authorize" button at top
   - Enter: `Bearer <your_access_token>`
   - Now you can access protected endpoints

## Client-Side Integration (Flutter/React)

### Option 1: Backend OTP (Current Implementation)
```javascript
// Send OTP
const response = await fetch('http://localhost:8000/auth/send-otp', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ phone_number: '+919876543210' })
});

// Verify OTP
const verifyResponse = await fetch('http://localhost:8000/auth/verify-otp', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ 
    phone_number: '+919876543210',
    otp_code: '123456'
  })
});

const { access_token } = await verifyResponse.json();
```

### Option 2: Firebase Client SDK (Recommended for Production)
```javascript
// In your Flutter/React app
import firebase from 'firebase/app';
import 'firebase/auth';

// Send OTP (handled by Firebase on client)
const confirmationResult = await firebase.auth()
  .signInWithPhoneNumber(phoneNumber, appVerifier);

// Verify OTP
const result = await confirmationResult.confirm(otpCode);
const idToken = await result.user.getIdToken();

// Send token to backend for verification
const response = await fetch('http://localhost:8000/auth/firebase-verify', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ id_token: idToken })
});
```

## Security Notes

1. **Never commit** `firebase-service-account.json` to version control
2. Add to `.gitignore`: `firebase-service-account.json`
3. In production, use environment variables for sensitive data
4. Enable Firebase App Check for additional security
5. Set up rate limiting to prevent OTP abuse

## Troubleshooting

### OTP Not Received in Production
- Check Firebase Console → Authentication → Phone numbers
- Verify phone number format (must include country code)
- Check Firebase quota limits
- Review Firebase logs

### Development Mode Not Working
- Check terminal output for OTP
- Verify database connection
- Check that phone number format is correct

### Token Verification Failed
- Ensure token is sent in Authorization header: `Bearer <token>`
- Check token expiration (default: 30 minutes)
- Verify SECRET_KEY in .env matches

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/auth/send-otp` | POST | Send OTP to phone number |
| `/auth/verify-otp` | POST | Verify OTP and get JWT token |
| `/auth/resend-otp` | POST | Resend OTP to phone number |

## Environment Variables

```bash
# Firebase (Optional - for production)
FIREBASE_SERVICE_ACCOUNT_KEY=firebase-service-account.json

# OTP Settings
OTP_EXPIRY_MINUTES=5
OTP_LENGTH=6

# JWT Settings
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Next Steps

1. Test the OTP flow in development mode
2. Set up Firebase project for production
3. Configure Firebase service account
4. Test with real phone numbers
5. Implement client-side Firebase SDK
6. Add rate limiting and security measures
