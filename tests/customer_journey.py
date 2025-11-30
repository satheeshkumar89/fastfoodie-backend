import sys
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from app.database import Base, get_db
from app.models import Owner, Restaurant, Category, MenuItem, RestaurantTypeEnum, VerificationStatusEnum

# Setup Test Client
client = TestClient(app)

# --- Helpers ---
def print_step(step):
    print(f"\n{'='*20} {step} {'='*20}")

def print_response(response):
    if response.status_code >= 400:
        print(f"FAILED: {response.status_code}")
        print(response.json())
    else:
        print("SUCCESS")
        # print(response.json()) # Uncomment for verbose output

# --- Setup Data ---
# We need to ensure there is at least one restaurant and menu item to test the flow
def setup_dummy_data():
    print_step("Setting up Dummy Data")
    # We need to manually create a session since we are outside the request scope
    # Assuming SQLite for simplicity in this dev environment, or using the app's DB config
    from app.database import SessionLocal
    db = SessionLocal()
    
    try:
        # 1. Create Owner
        owner = db.query(Owner).filter(Owner.email == "owner@test.com").first()
        if not owner:
            owner = Owner(
                full_name="Test Owner",
                email="owner@test.com",
                phone_number="+919999999999"
            )
            db.add(owner)
            db.commit()
            db.refresh(owner)
            print(f"Created Dummy Owner (ID: {owner.id})")
        else:
            print(f"Found Dummy Owner (ID: {owner.id})")
            
        # 2. Create Restaurant
        # Check by FSSAI first to avoid unique constraint error
        restaurant = db.query(Restaurant).filter(Restaurant.fssai_license_number == "12345678901234").first()
        if not restaurant:
            restaurant = Restaurant(
                owner_id=owner.id,
                restaurant_name="Test Spice Garden",
                restaurant_type=RestaurantTypeEnum.RESTAURANT,
                fssai_license_number="12345678901234",
                opening_time="10:00",
                closing_time="22:00",
                is_active=True,
                is_open=True,
                verification_status=VerificationStatusEnum.APPROVED,
                cost_for_two=500,
                description="Best food in town"
            )
            db.add(restaurant)
            db.commit()
            db.refresh(restaurant)
            print(f"Created Dummy Restaurant (ID: {restaurant.id})")
        else:
            print(f"Found Dummy Restaurant (ID: {restaurant.id})")
            
        # 3. Create Category
        category = db.query(Category).filter(Category.name == "Starters").first()
        if not category:
            category = Category(name="Starters", display_order=1)
            db.add(category)
            db.commit()
            db.refresh(category)
            print(f"Created Dummy Category (ID: {category.id})")
        else:
             print(f"Found Dummy Category (ID: {category.id})")
            
        # 4. Create Menu Item
        item = db.query(MenuItem).filter(MenuItem.restaurant_id == restaurant.id, MenuItem.name == "Paneer Tikka").first()
        if not item:
            item = MenuItem(
                restaurant_id=restaurant.id,
                category_id=category.id,
                name="Paneer Tikka",
                price=250.00,
                is_vegetarian=True,
                is_available=True
            )
            db.add(item)
            db.commit()
            db.refresh(item)
            print(f"Created Dummy Menu Item (ID: {item.id})")
        else:
            print(f"Found Dummy Menu Item (ID: {item.id})")
            
        return restaurant.id, item.id
        
    except Exception as e:
        print(f"Error setting up data: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        return None, None
    finally:
        db.close()

# --- Main Flow ---
def run_customer_flow():
    restaurant_id, menu_item_id = setup_dummy_data()
    if not restaurant_id:
        print("Failed to setup data. Exiting.")
        return

    # 1. Authentication
    print_step("1. Authentication")
    phone_number = "+918888888888"
    
    # Send OTP
    print("Sending OTP...")
    response = client.post("/customer/auth/send-otp", json={"phone_number": phone_number})
    print_response(response)
    assert response.status_code == 200
    otp = response.json()['data']['otp']
    print(f"Received OTP: {otp}")
    
    # Verify OTP
    print("Verifying OTP...")
    response = client.post("/customer/auth/verify-otp", json={"phone_number": phone_number, "otp_code": otp})
    print_response(response)
    assert response.status_code == 200
    token = response.json()['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    print("Got Access Token")

    # 2. Profile Setup
    print_step("2. Profile Setup")
    print("Updating Profile...")
    response = client.put("/customer/profile", headers=headers, json={
        "full_name": "Test Customer",
        "email": "customer@test.com"
    })
    print_response(response)
    assert response.status_code == 200
    print("Profile Updated")

    # 3. Home & Discovery
    print_step("3. Home & Discovery")
    print("Fetching Home Data...")
    response = client.get("/customer/home", headers=headers)
    print_response(response)
    assert response.status_code == 200
    
    print(f"Fetching Restaurant Details (ID: {restaurant_id})...")
    response = client.get(f"/customer/restaurants/{restaurant_id}", headers=headers)
    print_response(response)
    assert response.status_code == 200

    # 4. Address
    print_step("4. Address Management")
    print("Adding Address...")
    response = client.post("/customer/addresses", headers=headers, json={
        "latitude": 12.9716,
        "longitude": 77.5946,
        "address_line_1": "Test Flat 101",
        "city": "Bangalore",
        "state": "Karnataka",
        "pincode": "560001",
        "address_type": "home",
        "is_default": True
    })
    print_response(response)
    assert response.status_code == 200
    address_id = response.json()['data']['id']
    print(f"Address Created (ID: {address_id})")

    # 5. Cart & Order
    print_step("5. Cart & Order")
    print("Adding to Cart...")
    response = client.post("/customer/cart/add", headers=headers, json={
        "menu_item_id": menu_item_id,
        "quantity": 2,
        "restaurant_id": restaurant_id
    })
    print_response(response)
    assert response.status_code == 200
    
    print("Fetching Cart...")
    response = client.get("/customer/cart", headers=headers)
    print_response(response)
    assert response.status_code == 200
    cart_total = response.json()['data']['total_amount']
    print(f"Cart Total: {cart_total}")
    
    print("Placing Order...")
    response = client.post("/customer/orders", headers=headers, json={
        "restaurant_id": restaurant_id,
        "address_id": address_id,
        "payment_method": "UPI"
    })
    print_response(response)
    assert response.status_code == 200
    order_id = response.json()['data']['order_id']
    print(f"Order Placed (ID: {order_id})")

    # 6. Tracking
    print_step("6. Order Tracking")
    print(f"Tracking Order {order_id}...")
    response = client.get(f"/customer/orders/{order_id}/track", headers=headers)
    print_response(response)
    assert response.status_code == 200
    status = response.json()['data']['status']
    print(f"Order Status: {status}")
    
    print("\n\n✅ CUSTOMER FLOW TEST PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_customer_flow()
