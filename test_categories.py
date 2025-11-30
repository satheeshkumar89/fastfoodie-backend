#!/usr/bin/env python3
"""
Test script to verify the categories system is working
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_categories():
    """Test getting all categories"""
    print("🧪 Testing GET /menu/categories...")
    response = requests.get(f"{BASE_URL}/menu/categories")
    
    if response.status_code == 200:
        data = response.json()
        categories = data['data']['categories']
        print(f"✅ SUCCESS: Got {len(categories)} categories")
        print(f"\n📋 First 10 categories:")
        for cat in categories[:10]:
            print(f"   {cat['id']:2d}. {cat['name']}")
        return True
    else:
        print(f"❌ FAILED: Status {response.status_code}")
        print(response.text)
        return False


def get_auth_token():
    """Get authentication token"""
    print("\n🔐 Getting authentication token...")
    
    # Send OTP
    print("📱 Sending OTP to +453204589838...")
    otp_response = requests.post(
        f"{BASE_URL}/auth/send-otp",
        json={"phone_number": "+453204589838"}
    )
    
    if otp_response.status_code != 200:
        print(f"❌ Failed to send OTP: {otp_response.text}")
        return None
    
    otp_data = otp_response.json()
    otp_code = otp_data['data']['otp_code']
    print(f"✅ OTP sent: {otp_code}")
    
    # Verify OTP
    print("🔓 Verifying OTP...")
    verify_response = requests.post(
        f"{BASE_URL}/auth/verify-otp",
        json={
            "phone_number": "+453204589838",
            "otp_code": otp_code
        }
    )
    
    if verify_response.status_code != 200:
        print(f"❌ Failed to verify OTP: {verify_response.text}")
        return None
    
    verify_data = verify_response.json()
    token = verify_data['data']['access_token']
    print(f"✅ Got token: {token[:20]}...")
    return token


def test_menu_items(token):
    """Test getting menu items"""
    print("\n🧪 Testing GET /menu/items...")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/menu/items", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        items = data['data']['items']
        print(f"✅ SUCCESS: Got {len(items)} menu items")
        
        if items:
            print(f"\n📋 Menu items:")
            for item in items:
                cat_name = item['category']['name'] if item.get('category') else 'No category'
                print(f"   - {item['name']} (Category: {cat_name})")
        return True
    else:
        print(f"❌ FAILED: Status {response.status_code}")
        print(response.text)
        return False


def test_add_menu_item(token):
    """Test adding a menu item with category"""
    print("\n🧪 Testing POST /menu/item/add...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    new_item = {
        "name": "Margherita Pizza",
        "description": "Classic pizza with tomato sauce and mozzarella",
        "price": 299.00,
        "discount_price": 249.00,
        "category_id": 8,  # Pizzas
        "is_vegetarian": True,
        "is_available": True,
        "preparation_time": 20
    }
    
    response = requests.post(
        f"{BASE_URL}/menu/item/add",
        headers=headers,
        json=new_item
    )
    
    if response.status_code == 200:
        data = response.json()
        item = data['data']
        print(f"✅ SUCCESS: Added menu item '{item['name']}'")
        print(f"   Category: {item['category']['name']} (ID: {item['category_id']})")
        print(f"   Price: ₹{item['price']}")
        return True
    else:
        print(f"❌ FAILED: Status {response.status_code}")
        print(response.text)
        return False


def test_filter_by_category(token, category_id=8):
    """Test filtering menu items by category"""
    print(f"\n🧪 Testing GET /menu/items?category_id={category_id}...")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{BASE_URL}/menu/items?category_id={category_id}",
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        items = data['data']['items']
        print(f"✅ SUCCESS: Got {len(items)} items in category {category_id}")
        
        if items:
            print(f"\n📋 Items in this category:")
            for item in items:
                print(f"   - {item['name']} (₹{item['price']})")
        return True
    else:
        print(f"❌ FAILED: Status {response.status_code}")
        print(response.text)
        return False


def main():
    print("=" * 60)
    print("🍽️  FastFoodie Categories System Test")
    print("=" * 60)
    
    # Test 1: Get categories (no auth required)
    if not test_categories():
        print("\n❌ Categories test failed. Exiting.")
        return
    
    # Test 2: Get auth token
    token = get_auth_token()
    if not token:
        print("\n❌ Failed to get auth token. Exiting.")
        return
    
    # Test 3: Get menu items
    if not test_menu_items(token):
        print("\n⚠️  Menu items test failed, but continuing...")
    
    # Test 4: Add menu item with category
    if not test_add_menu_item(token):
        print("\n⚠️  Add menu item test failed, but continuing...")
    
    # Test 5: Filter by category
    if not test_filter_by_category(token, category_id=8):
        print("\n⚠️  Filter by category test failed.")
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
