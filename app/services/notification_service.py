from sqlalchemy.orm import Session
from app.models import Notification, DeviceToken
from typing import Optional

class NotificationService:
    @staticmethod
    async def send_order_update(
        db: Session,
        order_id: int, 
        status: str, 
        customer_id: Optional[int] = None, 
        owner_id: Optional[int] = None,
        delivery_partner_id: Optional[int] = None
    ):
        """
        Send order update notification and save to database.
        """
        if status == "rejected":
            title = f"Order #{order_id} Rejected"
            message = "Sorry, the restaurant cannot fulfill your order at this time."
        else:
            title = f"Order #{order_id} Update"
            message = f"Your order is now {status.replace('_', ' ')}."
        
        # Save to database for each relevant user
        if customer_id:
            await NotificationService.create_notification(
                db, 
                customer_id=customer_id,
                title=title,
                message=message,
                notification_type="order_update",
                order_id=order_id
            )
            
        if owner_id:
            await NotificationService.create_notification(
                db, 
                owner_id=owner_id,
                title=f"New Order Update #{order_id}",
                message=f"Order status changed to {status}",
                notification_type="order_update",
                order_id=order_id
            )

        print(f"Notification triggered for Order #{order_id} - Status: {status}")
        return True

    @staticmethod
    async def create_notification(
        db: Session,
        title: str,
        message: str,
        notification_type: str,
        owner_id: Optional[int] = None,
        customer_id: Optional[int] = None,
        delivery_partner_id: Optional[int] = None,
        order_id: Optional[int] = None
    ):
        notification = Notification(
            owner_id=owner_id,
            customer_id=customer_id,
            delivery_partner_id=delivery_partner_id,
            title=title,
            message=message,
            notification_type=notification_type,
            order_id=order_id
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)
        
        # TODO: Here we would trigger actual FCM push using device tokens
        # tokens = db.query(DeviceToken).filter(...)
        
        return notification

    @staticmethod
    def create_notification_sync(
        db: Session,
        title: str,
        message: str,
        notification_type: str,
        owner_id: Optional[int] = None,
        customer_id: Optional[int] = None,
        delivery_partner_id: Optional[int] = None,
        order_id: Optional[int] = None
    ):
        notification = Notification(
            owner_id=owner_id,
            customer_id=customer_id,
            delivery_partner_id=delivery_partner_id,
            title=title,
            message=message,
            notification_type=notification_type,
            order_id=order_id
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)
        return notification
