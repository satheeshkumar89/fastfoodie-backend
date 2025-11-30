"""
Seed realistic orders for testing the FastFoodie order flow
"""
import sys
import random
from datetime import datetime, timedelta
from decimal import Decimal
from sqlalchemy.orm import Session

# Add app to path
sys.path.append('.')

from app.database import SessionLocal
from app.models import Order, OrderItem, Restaurant, MenuItem, OrderStatusEnum

# Sample customer data
CUSTOMERS = [
    {"name": "Rajesh Kumar", "phone": "+919876543210"},
    {"name": "Priya Sharma", "phone": "+919876543211"},
    {"name": "Amit Patel", "phone": "+919876543212"},
    {"name": "Sneha Reddy", "phone": "+919876543213"},
    {"name": "Vikram Singh", "phone": "+919876543214"},
    {"name": "Anita Desai", "phone": "+919876543215"},
    {"name": "Rahul Mehta", "phone": "+919876543216"},
    {"name": "Kavita Joshi", "phone": "+919876543217"},
    {"name": "Suresh Nair", "phone": "+919876543218"},
    {"name": "Deepa Iyer", "phone": "+919876543219"},
    {"name": "Satheesh Kumar", "phone": "+918668109712"},  # Added specific customer
]

ADDRESSES = [
    "123 MG Road, Bangalore, Karnataka 560001",
    "456 Park Street, Kolkata, West Bengal 700016",
    "789 Marine Drive, Mumbai, Maharashtra 400002",
    "321 Connaught Place, New Delhi, Delhi 110001",
    "654 Anna Salai, Chennai, Tamil Nadu 600002",
    "987 FC Road, Pune, Maharashtra 411004",
    "147 Residency Road, Bangalore, Karnataka 560025",
    "258 Salt Lake, Kolkata, West Bengal 700091",
    "369 Bandra West, Mumbai, Maharashtra 400050",
    "741 Karol Bagh, New Delhi, Delhi 110005",
    "No 12, 1st Main, 2nd Cross, Indiranagar, Bangalore 560038", # Added address
]

SPECIAL_INSTRUCTIONS = [
    "Extra spicy please",
    "No onions",
    "Less oil",
    "Make it mild",
    "Extra cheese",
    "Well done",
    "Medium spicy",
    "No garlic",
    "Extra sauce on the side",
    "Pack separately",
    None,
    None,
    None,  # More likely to have no special instructions
]

PAYMENT_METHODS = ["cash", "card", "upi", "wallet"]


def generate_order_number():
    """Generate unique order number"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_num = random.randint(1000, 9999)
    return f"ORD{timestamp}{random_num}"


def create_new_orders(db: Session, restaurant_id: int, menu_items: list, count: int = 5):
    """Create new orders (status: NEW)"""
    print(f"\n📦 Creating {count} NEW orders...")
    orders_created = []
    
    for i in range(count):
        customer = random.choice(CUSTOMERS)
        
        # Select 1-4 random menu items
        num_items = random.randint(1, 4)
        selected_items = random.sample(menu_items, min(num_items, len(menu_items)))
        
        # Calculate totals
        subtotal = Decimal('0.00')
        order_items_data = []
        
        for item in selected_items:
            quantity = random.randint(1, 3)
            price = item.discount_price if item.discount_price else item.price
            item_total = Decimal(str(price)) * quantity
            subtotal += item_total
            
            order_items_data.append({
                'menu_item_id': item.id,
                'quantity': quantity,
                'price': price,
                'special_instructions': random.choice(SPECIAL_INSTRUCTIONS)
            })
        
        delivery_fee = Decimal('30.00')
        tax_amount = subtotal * Decimal('0.05')  # 5% tax
        discount = Decimal('0.00')
        total = subtotal + delivery_fee + tax_amount - discount
        
        # Create order
        order = Order(
            order_number=generate_order_number(),
            restaurant_id=restaurant_id,
            customer_name=customer['name'],
            customer_phone=customer['phone'],
            delivery_address=random.choice(ADDRESSES),
            status=OrderStatusEnum.NEW,
            total_amount=total,
            delivery_fee=delivery_fee,
            tax_amount=tax_amount,
            discount_amount=discount,
            payment_method=random.choice(PAYMENT_METHODS),
            payment_status="pending",
            special_instructions=random.choice(SPECIAL_INSTRUCTIONS),
            estimated_delivery_time=datetime.now() + timedelta(minutes=random.randint(30, 60)),
            created_at=datetime.now() - timedelta(minutes=random.randint(1, 15))
        )
        
        db.add(order)
        db.flush()
        
        # Add order items
        for item_data in order_items_data:
            order_item = OrderItem(
                order_id=order.id,
                **item_data
            )
            db.add(order_item)
        
        orders_created.append(order)
        print(f"  ✅ {order.order_number} - {customer['name']} - ₹{total}")
    
    db.commit()
    return orders_created


def create_ongoing_orders(db: Session, restaurant_id: int, menu_items: list, count: int = 8):
    """Create ongoing orders (status: ACCEPTED, PREPARING, READY, PICKED_UP)"""
    print(f"\n🔄 Creating {count} ONGOING orders...")
    orders_created = []
    
    statuses = [
        OrderStatusEnum.ACCEPTED,
        OrderStatusEnum.PREPARING,
        OrderStatusEnum.READY,
        OrderStatusEnum.PICKED_UP
    ]
    
    for i in range(count):
        customer = random.choice(CUSTOMERS)
        status = random.choice(statuses)
        
        # Select menu items
        num_items = random.randint(1, 4)
        selected_items = random.sample(menu_items, min(num_items, len(menu_items)))
        
        # Calculate totals
        subtotal = Decimal('0.00')
        order_items_data = []
        
        for item in selected_items:
            quantity = random.randint(1, 3)
            price = item.discount_price if item.discount_price else item.price
            item_total = Decimal(str(price)) * quantity
            subtotal += item_total
            
            order_items_data.append({
                'menu_item_id': item.id,
                'quantity': quantity,
                'price': price,
                'special_instructions': random.choice(SPECIAL_INSTRUCTIONS)
            })
        
        delivery_fee = Decimal('30.00')
        tax_amount = subtotal * Decimal('0.05')
        total = subtotal + delivery_fee + tax_amount
        
        # Create timestamps based on status
        created_time = datetime.now() - timedelta(minutes=random.randint(20, 60))
        accepted_time = created_time + timedelta(minutes=2)
        preparing_time = accepted_time + timedelta(minutes=5) if status in [OrderStatusEnum.PREPARING, OrderStatusEnum.READY, OrderStatusEnum.PICKED_UP] else None
        ready_time = preparing_time + timedelta(minutes=15) if status in [OrderStatusEnum.READY, OrderStatusEnum.PICKED_UP] else None
        pickedup_time = ready_time + timedelta(minutes=5) if status == OrderStatusEnum.PICKED_UP else None
        
        order = Order(
            order_number=generate_order_number(),
            restaurant_id=restaurant_id,
            customer_name=customer['name'],
            customer_phone=customer['phone'],
            delivery_address=random.choice(ADDRESSES),
            status=status,
            total_amount=total,
            delivery_fee=delivery_fee,
            tax_amount=tax_amount,
            payment_method=random.choice(PAYMENT_METHODS),
            payment_status="paid" if random.random() > 0.3 else "pending",
            special_instructions=random.choice(SPECIAL_INSTRUCTIONS),
            estimated_delivery_time=datetime.now() + timedelta(minutes=random.randint(10, 30)),
            created_at=created_time,
            accepted_at=accepted_time,
            preparing_at=preparing_time,
            ready_at=ready_time,
            pickedup_at=pickedup_time
        )
        
        db.add(order)
        db.flush()
        
        # Add order items
        for item_data in order_items_data:
            order_item = OrderItem(
                order_id=order.id,
                **item_data
            )
            db.add(order_item)
        
        orders_created.append(order)
        print(f"  ✅ {order.order_number} - {status.value.upper()} - {customer['name']} - ₹{total}")
    
    db.commit()
    return orders_created


def create_completed_orders(db: Session, restaurant_id: int, menu_items: list, count: int = 15):
    """Create completed orders (status: DELIVERED)"""
    print(f"\n✅ Creating {count} COMPLETED orders...")
    orders_created = []
    
    for i in range(count):
        customer = random.choice(CUSTOMERS)
        
        # Select menu items
        num_items = random.randint(1, 4)
        selected_items = random.sample(menu_items, min(num_items, len(menu_items)))
        
        # Calculate totals
        subtotal = Decimal('0.00')
        order_items_data = []
        
        for item in selected_items:
            quantity = random.randint(1, 3)
            price = item.discount_price if item.discount_price else item.price
            item_total = Decimal(str(price)) * quantity
            subtotal += item_total
            
            order_items_data.append({
                'menu_item_id': item.id,
                'quantity': quantity,
                'price': price,
                'special_instructions': random.choice(SPECIAL_INSTRUCTIONS)
            })
        
        delivery_fee = Decimal('30.00')
        tax_amount = subtotal * Decimal('0.05')
        discount = Decimal('20.00') if random.random() > 0.7 else Decimal('0.00')
        total = subtotal + delivery_fee + tax_amount - discount
        
        # Create realistic timestamps
        created_time = datetime.now() - timedelta(days=random.randint(0, 7), hours=random.randint(0, 23))
        accepted_time = created_time + timedelta(minutes=2)
        preparing_time = accepted_time + timedelta(minutes=5)
        ready_time = preparing_time + timedelta(minutes=20)
        pickedup_time = ready_time + timedelta(minutes=5)
        delivered_time = pickedup_time + timedelta(minutes=random.randint(15, 45))
        
        order = Order(
            order_number=generate_order_number(),
            restaurant_id=restaurant_id,
            customer_name=customer['name'],
            customer_phone=customer['phone'],
            delivery_address=random.choice(ADDRESSES),
            status=OrderStatusEnum.DELIVERED,
            total_amount=total,
            delivery_fee=delivery_fee,
            tax_amount=tax_amount,
            discount_amount=discount,
            payment_method=random.choice(PAYMENT_METHODS),
            payment_status="paid",
            special_instructions=random.choice(SPECIAL_INSTRUCTIONS),
            created_at=created_time,
            accepted_at=accepted_time,
            preparing_at=preparing_time,
            ready_at=ready_time,
            pickedup_at=pickedup_time,
            delivered_at=delivered_time,
            completed_at=delivered_time
        )
        
        db.add(order)
        db.flush()
        
        # Add order items
        for item_data in order_items_data:
            order_item = OrderItem(
                order_id=order.id,
                **item_data
            )
            db.add(order_item)
        
        orders_created.append(order)
        print(f"  ✅ {order.order_number} - {customer['name']} - ₹{total}")
    
    db.commit()
    return orders_created


def create_specific_customer_orders(db: Session, restaurant_id: int, menu_items: list):
    """Create specific orders for Satheesh Kumar (8668109712)"""
    print(f"\n👤 Creating specific orders for Satheesh Kumar (+918668109712)...")
    
    target_customer = {"name": "Satheesh Kumar", "phone": "+918668109712"}
    orders_created = []
    
    # 1. Create a NEW order
    order = Order(
        order_number=generate_order_number(),
        restaurant_id=restaurant_id,
        customer_name=target_customer['name'],
        customer_phone=target_customer['phone'],
        delivery_address="No 12, 1st Main, 2nd Cross, Indiranagar, Bangalore 560038",
        status=OrderStatusEnum.NEW,
        total_amount=Decimal('450.00'),
        delivery_fee=Decimal('30.00'),
        tax_amount=Decimal('20.00'),
        payment_method="upi",
        payment_status="paid",
        special_instructions="Ring the doorbell twice",
        estimated_delivery_time=datetime.now() + timedelta(minutes=45),
        created_at=datetime.now() - timedelta(minutes=5)
    )
    db.add(order)
    db.flush()
    
    # Add items
    item = menu_items[0] # First item
    order_item = OrderItem(order_id=order.id, menu_item_id=item.id, quantity=2, price=item.price)
    db.add(order_item)
    orders_created.append(order)
    print(f"  ✅ {order.order_number} - NEW - {target_customer['name']}")

    # 2. Create an ONGOING order (Preparing)
    order = Order(
        order_number=generate_order_number(),
        restaurant_id=restaurant_id,
        customer_name=target_customer['name'],
        customer_phone=target_customer['phone'],
        delivery_address="No 12, 1st Main, 2nd Cross, Indiranagar, Bangalore 560038",
        status=OrderStatusEnum.PREPARING,
        total_amount=Decimal('850.00'),
        delivery_fee=Decimal('30.00'),
        tax_amount=Decimal('40.00'),
        payment_method="card",
        payment_status="paid",
        estimated_delivery_time=datetime.now() + timedelta(minutes=25),
        created_at=datetime.now() - timedelta(minutes=20),
        accepted_at=datetime.now() - timedelta(minutes=15),
        preparing_at=datetime.now() - timedelta(minutes=5)
    )
    db.add(order)
    db.flush()
    
    # Add items
    if len(menu_items) > 1:
        item = menu_items[1]
        order_item = OrderItem(order_id=order.id, menu_item_id=item.id, quantity=1, price=item.price)
        db.add(order_item)
    orders_created.append(order)
    print(f"  ✅ {order.order_number} - PREPARING - {target_customer['name']}")

    # 3. Create a COMPLETED order
    order = Order(
        order_number=generate_order_number(),
        restaurant_id=restaurant_id,
        customer_name=target_customer['name'],
        customer_phone=target_customer['phone'],
        delivery_address="No 12, 1st Main, 2nd Cross, Indiranagar, Bangalore 560038",
        status=OrderStatusEnum.DELIVERED,
        total_amount=Decimal('320.00'),
        delivery_fee=Decimal('30.00'),
        tax_amount=Decimal('15.00'),
        payment_method="cash",
        payment_status="paid",
        created_at=datetime.now() - timedelta(days=1),
        accepted_at=datetime.now() - timedelta(days=1, minutes=-2),
        preparing_at=datetime.now() - timedelta(days=1, minutes=-5),
        ready_at=datetime.now() - timedelta(days=1, minutes=-20),
        pickedup_at=datetime.now() - timedelta(days=1, minutes=-25),
        delivered_at=datetime.now() - timedelta(days=1, minutes=-45),
        completed_at=datetime.now() - timedelta(days=1, minutes=-45)
    )
    db.add(order)
    db.flush()
    
    # Add items
    item = menu_items[0]
    order_item = OrderItem(order_id=order.id, menu_item_id=item.id, quantity=1, price=item.price)
    db.add(order_item)
    orders_created.append(order)
    print(f"  ✅ {order.order_number} - DELIVERED - {target_customer['name']}")

    db.commit()
    return orders_created


def main():
    print("=" * 60)
    print("🍽️  FastFoodie Order Seeder")
    print("=" * 60)
    
    db = SessionLocal()
    
    try:
        # Get restaurant
        restaurant = db.query(Restaurant).filter(Restaurant.is_active == True).first()
        
        if not restaurant:
            print("❌ No active restaurant found. Please create a restaurant first.")
            return
        
        print(f"\n🏪 Restaurant: {restaurant.restaurant_name}")
        print(f"   Owner ID: {restaurant.owner_id}")
        
        # Get menu items
        menu_items = db.query(MenuItem).filter(
            MenuItem.restaurant_id == restaurant.id,
            MenuItem.is_available == True
        ).all()
        
        if not menu_items:
            print("❌ No menu items found. Please add menu items first.")
            return
        
        print(f"   Menu Items: {len(menu_items)} available")
        
        # Create specific orders for Satheesh Kumar first
        specific_orders = create_specific_customer_orders(db, restaurant.id, menu_items)

        # Create random orders
        new_orders = create_new_orders(db, restaurant.id, menu_items, count=5)
        ongoing_orders = create_ongoing_orders(db, restaurant.id, menu_items, count=8)
        completed_orders = create_completed_orders(db, restaurant.id, menu_items, count=15)
        
        print("\n" + "=" * 60)
        print("✅ Order Seeding Complete!")
        print("=" * 60)
        print(f"\n📊 Summary:")
        print(f"   Specific Orders (Satheesh): {len(specific_orders)}")
        print(f"   NEW Orders: {len(new_orders)}")
        print(f"   ONGOING Orders: {len(ongoing_orders)}")
        print(f"   COMPLETED Orders: {len(completed_orders)}")
        print(f"   TOTAL: {len(new_orders) + len(ongoing_orders) + len(completed_orders) + len(specific_orders)}")
        
        print("\n🎯 Test the endpoints:")
        print("   GET /orders/new")
        print("   GET /orders/ongoing")
        print("   GET /orders/completed")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
