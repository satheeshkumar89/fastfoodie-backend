from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)

def check_user_notifications(phone_number):
    print(f"--- Checking Notifications for {phone_number} ---")
    
    # 1. Login to get token
    resp = client.post("/customer/auth/send-otp", json={"phone_number": phone_number})
    if resp.status_code != 200:
        print(f"❌ Failed to send OTP: {resp.text}")
        return
    
    otp = resp.json()['data']['otp']
    resp = client.post("/customer/auth/verify-otp", json={"phone_number": phone_number, "otp_code": otp})
    if resp.status_code != 200:
        print(f"❌ Failed to verify OTP: {resp.text}")
        return
        
    token = resp.json()['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Fetch Notifications
    resp = client.get("/notifications/customer", headers=headers)
    if resp.status_code == 200:
        notifications = resp.json().get('data', [])
        print(f"✅ Found {len(notifications)} notifications:")
        for n in notifications:
            print(f"  - [{n['created_at']}] {n['title']}: {n['message']} (Read: {n['is_read']})")
    else:
        print(f"❌ Failed to fetch notifications: {resp.status_code} {resp.text}")

if __name__ == "__main__":
    # Test with the provided number
    # Use +91 prefix as it's common in your DB
    phone = "+918668109715"
    check_user_notifications(phone)
