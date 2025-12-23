from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)

def test_proceed_pay_error():
    # 1. Login
    customer_phone = "+917766554433"
    resp = client.post("/customer/auth/send-otp", json={"phone_number": customer_phone})
    otp = resp.json()['data']['otp']
    resp = client.post("/customer/auth/verify-otp", json={"phone_number": customer_phone, "otp_code": otp})
    token = resp.json()['access_token']
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Get a restaurant and menu item
    # Spice Garden (ID 1) should have items if seeded
    resp = client.get("/customer/restaurants/1", headers=headers)
    restaurant_data = resp.json()['data']
    menu_items = restaurant_data.get('menu', [])
    if not menu_items:
        print("No menu items found for restaurant 1. Seeding one...")
        # Add a menu item manually if needed, but usually they are seeded
        # Or just use the one from home data
        pass
    else:
        item_id = menu_items[0]['id']
        print(f"Adding item {item_id} to cart...")
        client.post("/customer/cart/add", headers=headers, json={
            "menu_item_id": item_id,
            "quantity": 1,
            "restaurant_id": 1
        })

    # 3. Place order
    order_data = {
        "restaurant_id": 1,
        "address_id": 1,
        "payment_method": "UPI"
    }
    
    print("Testing /customer/orders...")
    resp = client.post("/customer/orders", headers=headers, json=order_data)
    print(f"Response Status: {resp.status_code}")
    print(f"Response Body: {resp.json()}")

if __name__ == "__main__":
    test_proceed_pay_error()
