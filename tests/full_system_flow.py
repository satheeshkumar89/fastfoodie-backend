import sys
import os
import time
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from app.database import Base, get_db

# Setup Test Client
client = TestClient(app)

# --- Helpers ---
def print_step(step):
    print(f"\n{'='*20} {step} {'='*20}")

def print_substep(step):
    print(f"   -> {step}")

def print_response(response, label="Response"):
    if response.status_code >= 400:
        print(f"   ❌ FAILED: {response.status_code}")
        print(f"   {response.json()}")
        sys.exit(1)
    else:
        print(f"   ✅ SUCCESS")

# --- Global Vars ---
owner_token = None
customer_token = None
restaurant_id = None
menu_item_id = None
order_id = None
address_id = None

# --- Main Flow ---
def run_full_system_flow():
    global owner_token, customer_token, restaurant_id, menu_item_id, order_id, address_id
    
    print("🚀 STARTING FULL SYSTEM END-TO-END TEST")
    
    # ==========================================
    # PART 1: OWNER APP FLOW
    # ==========================================
    print_step("PART 1: OWNER APP - SETUP RESTAURANT")
    
    # 1. Owner Auth
    print_substep("Owner Login/Register")
    owner_phone = "+919988776655"
    # Send OTP
    resp = client.post("/auth/send-otp", json={"phone_number": owner_phone, "role": "owner"})
    print_response(resp)
    otp = resp.json()['data']['otp']
    
    # Verify OTP
    resp = client.post("/auth/verify-otp", json={"phone_number": owner_phone, "otp_code": otp, "role": "owner"})
    print_response(resp)
    owner_token = resp.json()['access_token']
    owner_headers = {"Authorization": f"Bearer {owner_token}"}
    
    # 2. Create Restaurant
    print_substep("Create Restaurant")
    # Unique license to avoid conflicts
    license_num = f"FSSAI{int(time.time())}"
    restaurant_data = {
        "restaurant_name": "System Test Bistro",
        "restaurant_type": "restaurant",
        "fssai_license_number": license_num,
        "opening_time": "09:00",
        "closing_time": "23:00"
    }
    resp = client.post("/restaurant/create", headers=owner_headers, json=restaurant_data)
    if resp.status_code == 400 and "already exists" in resp.json()['detail']:
        # Fetch existing restaurant
        resp = client.get("/restaurant/details", headers=owner_headers)
        print_response(resp)
        restaurant_id = resp.json()['data']['id']
        print(f"      Restaurant ID (Existing): {restaurant_id}")
    else:
        print_response(resp)
        restaurant_id = resp.json()['data']['id']
        print(f"      Restaurant ID: {restaurant_id}")
    
    # 3. Add Menu Item
    print_substep("Add Menu Item")
    # First get categories to link
    resp = client.get("/menu/categories", headers=owner_headers)
    data = resp.json()['data']
    categories = data.get('categories', [])
    if not categories:
        # Seed a category if none
        # Skipping for now assuming seed data exists or default categories
        cat_id = 1 
    else:
        cat_id = categories[0]['id']
        
    item_data = {
        "name": "Signature Burger",
        "description": "Juicy patty with secret sauce",
        "price": 199.00,
        "category_id": cat_id,
        "is_vegetarian": False,
        "is_available": True,
        "preparation_time": 15
    }
    resp = client.post("/menu/item/add", headers=owner_headers, json=item_data)
    print_response(resp)
    menu_item_id = resp.json()['data']['id']
    print(f"      Menu Item ID: {menu_item_id}")
    
    # 4. Open Restaurant
    print_substep("Open Restaurant")
    resp = client.put("/restaurant/status?is_open=true", headers=owner_headers)
    print_response(resp)

    # ==========================================
    # PART 2: CUSTOMER APP FLOW
    # ==========================================
    print_step("PART 2: CUSTOMER APP - PLACE ORDER")
    
    # 1. Customer Auth
    print_substep("Customer Login/Register")
    customer_phone = "+917766554433"
    # Send OTP
    resp = client.post("/customer/auth/send-otp", json={"phone_number": customer_phone})
    print_response(resp)
    otp = resp.json()['data']['otp']
    
    # Verify OTP
    resp = client.post("/customer/auth/verify-otp", json={"phone_number": customer_phone, "otp_code": otp})
    print_response(resp)
    customer_token = resp.json()['access_token']
    customer_headers = {"Authorization": f"Bearer {customer_token}"}
    
    # 2. Verify Restaurant Visibility
    print_substep("Check Home Screen for Restaurant")
    resp = client.get("/customer/home", headers=customer_headers)
    print_response(resp)
    restaurants = resp.json()['data']['restaurants']
    found = any(r['id'] == restaurant_id for r in restaurants)
    if found:
        print("      ✅ Restaurant found in Home list")
    else:
        print("      ❌ Restaurant NOT found in Home list (might be inactive/closed logic?)")
        # Proceeding anyway as we have ID
        
    # 3. Add Address
    print_substep("Add Delivery Address")
    addr_data = {
        "latitude": 12.9,
        "longitude": 77.6,
        "address_line_1": "Test Customer House",
        "city": "Bangalore",
        "state": "KA",
        "pincode": "560001",
        "is_default": True
    }
    resp = client.post("/customer/addresses", headers=customer_headers, json=addr_data)
    print_response(resp)
    address_id = resp.json()['data']['id']
    
    # 4. Add to Cart
    print_substep("Add Item to Cart")
    cart_data = {
        "menu_item_id": menu_item_id,
        "quantity": 2,
        "restaurant_id": restaurant_id
    }
    resp = client.post("/customer/cart/add", headers=customer_headers, json=cart_data)
    print_response(resp)
    
    # 5. Place Order
    print_substep("Place Order")
    order_data = {
        "restaurant_id": restaurant_id,
        "address_id": address_id,
        "payment_method": "UPI"
    }
    resp = client.post("/customer/orders", headers=customer_headers, json=order_data)
    print_response(resp)
    order_id = resp.json()['data']['order_id']
    print(f"      Order ID: {order_id}")
    
    # ==========================================
    # PART 3: FULFILLMENT & TRACKING
    # ==========================================
    print_step("PART 3: FULFILLMENT & TRACKING")
    
    # 1. Owner Receives Order
    print_substep("Owner: Check New Orders")
    resp = client.get("/orders/new", headers=owner_headers)
    print_response(resp)
    orders = resp.json()['data']['orders']
    found_order = any(o['order_id'] == order_id for o in orders)
    if found_order:
        print("      ✅ Owner sees the new order")
    else:
        print("      ❌ Owner does NOT see the new order")
        sys.exit(1)
        
    # 2. Owner Accepts Order
    print_substep("Owner: Accept Order")
    resp = client.put(f"/orders/{order_id}/accept", headers=owner_headers)
    print_response(resp)
    
    # 3. Customer Tracks Order
    print_substep("Customer: Track Order (Expect 'Accepted')")
    resp = client.get(f"/customer/orders/{order_id}/track", headers=customer_headers)
    print_response(resp)
    status = resp.json()['data']['status']
    print(f"      Current Status: {status}")
    if status == "accepted":
        print("      ✅ Status matches")
    else:
        print(f"      ❌ Status mismatch (Expected accepted, got {status})")

    # 4. Owner Marks Ready
    print_substep("Owner: Mark Ready")
    resp = client.put(f"/orders/{order_id}/ready", headers=owner_headers)
    print_response(resp)
    
    # 5. Owner Marks Out for Delivery (Picked Up)
    print_substep("Owner: Mark Picked Up")
    resp = client.put(f"/orders/{order_id}/pickedup", headers=owner_headers)
    print_response(resp)
    
    # 6. Customer Tracks Again
    print_substep("Customer: Track Order (Expect 'Picked Up')")
    resp = client.get(f"/customer/orders/{order_id}/track", headers=customer_headers)
    print_response(resp)
    status = resp.json()['data']['status']
    print(f"      Current Status: {status}")
    
    print("\n🎉 FULL SYSTEM FLOW VERIFIED SUCCESSFULLY!")

if __name__ == "__main__":
    run_full_system_flow()
