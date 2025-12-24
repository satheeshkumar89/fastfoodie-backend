from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)

def verify_new_order_notification():
    print("--- Verifying 'New Order' Notification Flow ---")
    
    # 1. Setup - Use existing owner (+919999999999) and customer (+917766554433)
    # Get Owner Token
    owner_phone = "+919999999999"
    resp = client.post("/owner/auth/send-otp", json={"phone_number": owner_phone})
    otp = resp.json()['data']['otp']
    resp = client.post("/owner/auth/verify-otp", json={"phone_number": owner_phone, "otp_code": otp})
    owner_token = resp.json()['access_token']
    owner_headers = {"Authorization": f"Bearer {owner_token}"}

    # Get Customer Token
    customer_phone = "+917766554433"
    resp = client.post("/customer/auth/send-otp", json={"phone_number": customer_phone})
    otp = resp.json()['data']['otp']
    resp = client.post("/customer/auth/verify-otp", json={"phone_number": customer_phone, "otp_code": otp})
    customer_token = resp.json()['access_token']
    customer_headers = {"Authorization": f"Bearer {customer_token}"}

    # 2. Customer adds item to cart and places order
    # Let's use Restaurant 1 (Spice Garden) which belongs to Owner 1
    print("Customer placing order...")
    client.post("/customer/cart/add", headers=customer_headers, json={
        "menu_item_id": 1,
        "quantity": 1,
        "restaurant_id": 1
    })
    
    resp = client.post("/customer/orders", headers=customer_headers, json={
        "restaurant_id": 1,
        "address_id": 1,
        "payment_method": "UPI"
    })
    
    if resp.status_code == 200:
        order_num = resp.json()['data']['order_number']
        print(f"✅ Order {order_num} placed successfully.")
    else:
        print(f"❌ Failed to place order: {resp.text}")
        return

    # 3. Check Owner's notification history for "New Order Received!"
    print("Checking Owner's notifications...")
    resp = client.get("/notifications", headers=owner_headers)
    if resp.status_code == 200:
        notifications = resp.json().get('data', [])
        found = False
        for n in notifications:
            if n['title'] == "New Order Received!":
                print(f"✅ Found Notification: {n['title']} - {n['message']}")
                found = True
                break
        if not found:
            print("❌ Notification 'New Order Received!' NOT found in owner history.")
    else:
        print(f"❌ Failed to fetch owner notifications: {resp.text}")

if __name__ == "__main__":
    verify_new_order_notification()
