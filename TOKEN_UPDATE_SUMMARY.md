# ✅ Token Expiration Updated

**Status:** 🟢 **UPDATED**

The authentication token expiration time has been increased to **7 days**.

---

## 🔧 Changes Made

1. **Updated `.env` file:**
   ```bash
   ACCESS_TOKEN_EXPIRE_MINUTES=10080  # 7 days * 24h * 60m
   ```

2. **Updated `app/config.py`:**
   ```python
   ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080
   ```

3. **Restarted Server:**
   - Server was restarted to apply the new configuration.

---

## 🧪 Verification

Any **newly generated tokens** will now be valid for 7 days.

**To get a new 7-day token:**
1. Send OTP: `POST /auth/send-otp`
2. Verify OTP: `POST /auth/verify-otp`

The returned `access_token` will have an expiration time of 7 days from now.

---

## 📝 Note for Flutter App

You don't need to change anything in your Flutter app code. Just log in again to get a long-lived token.
