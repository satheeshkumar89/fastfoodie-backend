import sys
import os
import time
from fastapi.testclient import TestClient

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from app.database import Base, engine, SessionLocal
from app.models import Owner, Customer, Order, Restaurant, OrderStatusEnum

client = TestClient(app)

def test_notification_flow():
    print("🚀 Testing Notification Flow...")

    # 1. Owner Login
    print("\n1. Logging in as Owner...")
    owner_phone = "+919988776655"
    resp = client.post("/auth/send-otp", json={"phone_number": owner_phone, "role": "owner"})
    otp = resp.json()['data']['otp']
    resp = client.post("/auth/verify-otp", json={"phone_number": owner_phone, "otp_code": otp, "role": "owner"})
    owner_token = resp.json()['access_token']
    owner_headers = {"Authorization": f"Bearer {owner_token}"}
    print("✅ Owner logged in.")

    # 2. Register Device Token for Owner
    print("\n2. Registering Device Token for Owner...")
    device_token_data = {
        "token": "test_owner_fcm_token_" + str(int(time.time())),
        "device_type": "android"
    }
    resp = client.post("/notifications/device-token", headers=owner_headers, json=device_token_data)
    print(f"Response: {resp.json()}")
    assert resp.status_code == 200
    print("✅ Owner device token registered.")

    # 3. Customer Login
    print("\n3. Logging in as Customer...")
    customer_phone = "+917766554433"
    resp = client.post("/customer/auth/send-otp", json={"phone_number": customer_phone})
    otp = resp.json()['data']['otp']
    resp = client.post("/customer/auth/verify-otp", json={"phone_number": customer_phone, "otp_code": otp})
    customer_token = resp.json()['access_token']
    customer_headers = {"Authorization": f"Bearer {customer_token}"}
    print("✅ Customer logged in.")

    # 4. Register Device Token for Customer
    print("\n4. Registering Device Token for Customer...")
    customer_device_token = {
        "token": "test_customer_fcm_token_" + str(int(time.time())),
        "device_type": "ios"
    }
    resp = client.post("/notifications/customer/device-token", headers=customer_headers, json=customer_device_token)
    print(f"Response: {resp.json()}")
    assert resp.status_code == 200
    print("✅ Customer device token registered.")

    # Ensure there is a restaurant for this owner
    db = SessionLocal()
    restaurant = db.query(Restaurant).filter(Restaurant.owner_id == 2).first()
    if not restaurant:
        print("\nCreating a test restaurant for Owner 2...")
        restaurant = Restaurant(
            owner_id=2,
            restaurant_name="Test Notification Restaurant",
            restaurant_type="restaurant",
            fssai_license_number="FSSAI123456789",
            opening_time="09:00",
            closing_time="22:00",
            is_active=True,
            is_open=True,
            verification_status="approved"
        )
        db.add(restaurant)
        db.commit()
        db.refresh(restaurant)
        print(f"✅ Restaurant created with ID: {restaurant.id}")
    else:
        # Ensure it's open for the test
        restaurant.is_open = True
        restaurant.is_active = True
        restaurant.verification_status = "approved"
        db.commit()
    
    restaurant_id = restaurant.id

    # 5. Triggering Notification via Order Update...
    print("\n5. Triggering Notification via Order Update...")
    
    # Ensure there's an order for this restaurant
    order = db.query(Order).filter(Order.restaurant_id == restaurant_id).first()
    if not order:
        print("Creating a test order...")
        order = Order(
            order_number="NOTIF-TEST-001",
            restaurant_id=restaurant_id,
            customer_id=2, # The customer we logged in as
            customer_name="Test Customer",
            customer_phone=customer_phone,
            delivery_address="123 Test Street",
            status=OrderStatusEnum.NEW,
            total_amount=500.0,
            payment_status="success"
        )
        db.add(order)
        db.commit()
        db.refresh(order)
        print(f"✅ Order created with ID: {order.id}")
    
    order_id = order.id
    db.close()

    # Update order status to 'accepted' which triggers a notification
    # Note: We need restaurant headers for /orders endpoints
    # For testing purposes, we can use the owner_token if the owner owns the restaurant
    # In this app, get_current_restaurant dependency uses the owner's token to find their restaurant.
    
    resp = client.put(f"/orders/{order_id}/accept", headers=owner_headers)
    print(f"Update Status Response: {resp.status_code}")
    if resp.status_code != 200:
        print(f"❌ Failed to update order status: {resp.json()}")
        return

    print("✅ Order status updated. Notification should be generated.")

    # 6. Check Notifications for Customer
    print("\n6. Checking Notifications for Customer...")
    resp = client.get("/notifications/customer", headers=customer_headers)
    notifications = resp.json()['data']
    print(f"Found {len(notifications)} notifications for customer.")
    
    found = False
    for n in notifications:
        print(f"  - [{n['created_at']}] {n['title']}: {n['message']}")
        if f"Order #{order_id}" in n['title'] or f"Order #{order_id}" in n['message']:
            found = True
            notification_id = n['id']
    
    if found:
        print("✅ Success! Notification found in customer history.")
        
        # 7. Mark as Read
        print(f"\n7. Marking Notification {notification_id} as read...")
        resp = client.put(f"/notifications/{notification_id}/read", headers=customer_headers)
        print(f"Response: {resp.json()}")
        assert resp.status_code == 200
        print("✅ Notification marked as read.")
    else:
        print("❌ Notification NOT found in customer history.")

    # 8. Check Notifications for Owner
    print("\n8. Checking Notifications for Owner...")
    resp = client.get("/notifications", headers=owner_headers)
    notifications = resp.json()['data']
    print(f"Found {len(notifications)} notifications for owner.")
    for n in notifications:
        print(f"  - [{n['created_at']}] {n['title']}: {n['message']}")

if __name__ == "__main__":
    test_notification_flow()
