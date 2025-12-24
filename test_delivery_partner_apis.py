#!/usr/bin/env python3
"""
Test script for Delivery Partner APIs
"""

import requests
import json

# Base URL
BASE_URL = "http://localhost:8000"

def print_response(title, response):
    print(f"\n{'='*60}")
    print(f"📍 {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")
    print(f"{'='*60}\n")

def test_delivery_partner_apis():
    print("\n🚴 TESTING DELIVERY PARTNER APIs\n")
    
    # Test 1: Send OTP
    print("Test 1: Send OTP")
    phone = "+919876543999"  # Test phone number
    response = requests.post(
        f"{BASE_URL}/delivery-partner/auth/send-otp",
        json={"phone_number": phone}
    )
    print_response("Send OTP", response)
    
    if response.status_code == 200:
        otp_data = response.json()
        otp_code = otp_data.get("data", {}).get("otp", "123456")  # Get OTP from response or use default
        
        # Test 2: Verify OTP
        print("\nTest 2: Verify OTP")
        response = requests.post(
            f"{BASE_URL}/delivery-partner/auth/verify-otp",
            json={"phone_number": phone, "otp_code": otp_code}
        )
        print_response("Verify OTP", response)
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get("access_token")
            delivery_partner = token_data.get("delivery_partner")
            
            print(f"✅ Authentication Successful!")
            print(f"   Delivery Partner ID: {delivery_partner.get('id')}")
            print(f"   Name: {delivery_partner.get('full_name')}")
            print(f"   Phone: {delivery_partner.get('phone_number')}")
            
            # Set headers for authenticated requests
            headers = {"Authorization": f"Bearer {access_token}"}
            
            # Test 3: Get Profile
            print("\n\nTest 3: Get Profile")
            response = requests.get(
                f"{BASE_URL}/delivery-partner/profile",
                headers=headers
            )
            print_response("Get Profile", response)
            
            # Test 4: Update Profile
            print("\nTest 4: Update Profile")
            response = requests.put(
                f"{BASE_URL}/delivery-partner/profile",
                headers=headers,
                json={
                    "full_name": "Test Delivery Partner",
                    "vehicle_number": "KA01TEST1234"
                }
            )
            print_response("Update Profile", response)
            
            # Test 5: Get Available Orders
            print("\nTest 5: Get Available Orders")
            response = requests.get(
                f"{BASE_URL}/delivery-partner/orders/available",
                headers=headers
            )
            print_response("Available Orders", response)
            
            # Test 6: Get Active Orders
            print("\nTest 6: Get Active Orders")
            response = requests.get(
                f"{BASE_URL}/delivery-partner/orders/active",
                headers=headers
            )
            print_response("Active Orders", response)
            
            # Test 7: Get Completed Orders
            print("\nTest 7: Get Completed Orders")
            response = requests.get(
                f"{BASE_URL}/delivery-partner/orders/completed",
                headers=headers
            )
            print_response("Completed Orders", response)
            
            # Test 8: Get Earnings
            print("\nTest 8: Get Earnings")
            response = requests.get(
                f"{BASE_URL}/delivery-partner/earnings",
                headers=headers
            )
            print_response("Earnings", response)
            
            # Test 9: Get Notifications
            print("\nTest 9: Get Notifications")
            response = requests.get(
                f"{BASE_URL}/delivery-partner/notifications",
                headers=headers
            )
            print_response("Notifications", response)
            
            # Test 10: Register Device Token
            print("\nTest 10: Register Device Token")
            response = requests.post(
                f"{BASE_URL}/delivery-partner/device-token",
                headers=headers,
                json={
                    "token": "test_fcm_token_123456",
                    "device_type": "android"
                }
            )
            print_response("Register Device Token", response)
            
            print("\n" + "="*60)
            print("✅ ALL TESTS COMPLETED!")
            print("="*60)
            
        else:
            print("❌ OTP Verification failed!")
    else:
        print("❌ Send OTP failed!")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚴 DELIVERY PARTNER API TEST SUITE")
    print("="*60)
    print("\n⚠️  Make sure the FastAPI server is running on http://localhost:8000")
    print("   Run: python3 -m uvicorn app.main:app --reload\n")
    
    try:
        # Check if server is running
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        if response.status_code == 200:
            print("✅ Server is running!\n")
            test_delivery_partner_apis()
        else:
            print("❌ Server returned error!")
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running! Please start it first.")
    except Exception as e:
        print(f"❌ Error: {e}")
