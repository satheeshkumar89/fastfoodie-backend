from sqlalchemy.orm import Session
from app.models import Restaurant, VerificationStatusEnum
from datetime import datetime


class VerificationService:
    @staticmethod
    def submit_for_verification(db: Session, restaurant_id: int) -> bool:
        """Submit restaurant for verification"""
        restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
        
        if not restaurant:
            return False
        
        # Check if all required information is provided
        if not restaurant.address:
            raise ValueError("Restaurant address is required")
        
        # Check if documents are uploaded
        documents = restaurant.documents
        has_fssai = any(doc.document_type == "fssai_license" for doc in documents)
        has_photo = any(doc.document_type == "restaurant_photo" for doc in documents)
        
        if not has_fssai or not has_photo:
            raise ValueError("FSSAI license and restaurant photo are required")
        
        # Update verification status
        restaurant.verification_status = VerificationStatusEnum.SUBMITTED
        db.commit()
        
        return True
    
    @staticmethod
    def get_verification_status(db: Session, restaurant_id: int) -> dict:
        """Get verification status of restaurant"""
        restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
        
        if not restaurant:
            return None
        
        return {
            "status": restaurant.verification_status.value,
            "verification_notes": restaurant.verification_notes,
            "updated_at": restaurant.updated_at
        }
    
    @staticmethod
    def update_verification_status(
        db: Session, 
        restaurant_id: int, 
        status: VerificationStatusEnum,
        notes: str = None
    ) -> bool:
        """Update verification status (admin function)"""
        restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
        
        if not restaurant:
            return False
        
        restaurant.verification_status = status
        restaurant.verification_notes = notes
        db.commit()
        
        return True
