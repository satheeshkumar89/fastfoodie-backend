from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import APIResponse
from app.models import Restaurant, VerificationStatusEnum
from app.services.verification_service import VerificationService
from pydantic import BaseModel

router = APIRouter(prefix="/admin", tags=["Admin"])


class UpdateVerificationRequest(BaseModel):
    """Request schema for updating verification status"""
    status: str  # "approved" or "rejected" or "under_review"
    notes: str = None


@router.get("/restaurants/pending", response_model=APIResponse)
def get_pending_restaurants(db: Session = Depends(get_db)):
    """Get all restaurants pending verification (Admin only)"""
    restaurants = db.query(Restaurant).filter(
        Restaurant.verification_status.in_([
            VerificationStatusEnum.SUBMITTED,
            VerificationStatusEnum.UNDER_REVIEW
        ])
    ).all()
    
    restaurant_list = []
    for restaurant in restaurants:
        restaurant_list.append({
            "id": restaurant.id,
            "restaurant_name": restaurant.restaurant_name,
            "restaurant_type": restaurant.restaurant_type.value if restaurant.restaurant_type else None,
            "fssai_license_number": restaurant.fssai_license_number,
            "verification_status": restaurant.verification_status.value,
            "verification_notes": restaurant.verification_notes,
            "owner_name": restaurant.owner.full_name if restaurant.owner else None,
            "owner_phone": restaurant.owner.phone_number if restaurant.owner else None,
            "created_at": restaurant.created_at,
            "updated_at": restaurant.updated_at
        })
    
    return APIResponse(
        success=True,
        message=f"Found {len(restaurant_list)} restaurants pending verification",
        data={"restaurants": restaurant_list}
    )


@router.get("/restaurants/{restaurant_id}/details", response_model=APIResponse)
def get_restaurant_verification_details(
    restaurant_id: int,
    db: Session = Depends(get_db)
):
    """Get detailed information for restaurant verification (Admin only)"""
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )
    
    # Get documents
    documents = []
    for doc in restaurant.documents:
        documents.append({
            "document_type": doc.document_type,
            "file_url": doc.file_url,
            "file_name": doc.file_name,
            "uploaded_at": doc.created_at
        })
    
    # Get address
    address_data = None
    if restaurant.address:
        address_data = {
            "address_line_1": restaurant.address.address_line_1,
            "address_line_2": restaurant.address.address_line_2,
            "city": restaurant.address.city,
            "state": restaurant.address.state,
            "pincode": restaurant.address.pincode,
            "landmark": restaurant.address.landmark,
            "latitude": float(restaurant.address.latitude) if restaurant.address.latitude else None,
            "longitude": float(restaurant.address.longitude) if restaurant.address.longitude else None
        }
    
    # Get cuisines
    cuisines = [rc.cuisine.name for rc in restaurant.cuisines if rc.cuisine]
    
    return APIResponse(
        success=True,
        message="Restaurant details retrieved successfully",
        data={
            "restaurant": {
                "id": restaurant.id,
                "restaurant_name": restaurant.restaurant_name,
                "restaurant_type": restaurant.restaurant_type.value if restaurant.restaurant_type else None,
                "fssai_license_number": restaurant.fssai_license_number,
                "opening_time": str(restaurant.opening_time) if restaurant.opening_time else None,
                "closing_time": str(restaurant.closing_time) if restaurant.closing_time else None,
                "verification_status": restaurant.verification_status.value,
                "verification_notes": restaurant.verification_notes,
                "is_open": restaurant.is_open,
                "created_at": restaurant.created_at
            },
            "owner": {
                "full_name": restaurant.owner.full_name if restaurant.owner else None,
                "email": restaurant.owner.email if restaurant.owner else None,
                "phone_number": restaurant.owner.phone_number if restaurant.owner else None
            },
            "address": address_data,
            "cuisines": cuisines,
            "documents": documents
        }
    )


@router.put("/restaurants/{restaurant_id}/verify", response_model=APIResponse)
def update_verification_status(
    restaurant_id: int,
    verification_data: UpdateVerificationRequest,
    db: Session = Depends(get_db)
):
    """Update restaurant verification status (Admin only)"""
    try:
        # Validate status
        valid_statuses = ["under_review", "approved", "rejected"]
        if verification_data.status not in valid_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status. Must be one of: {valid_statuses}"
            )
        
        # Convert string to enum
        status_enum = VerificationStatusEnum(verification_data.status)
        
        # Update status
        success = VerificationService.update_verification_status(
            db=db,
            restaurant_id=restaurant_id,
            status=status_enum,
            notes=verification_data.notes
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found"
            )
        
        # Get updated restaurant
        restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
        
        return APIResponse(
            success=True,
            message=f"Restaurant verification status updated to {verification_data.status}",
            data={
                "restaurant_id": restaurant_id,
                "status": restaurant.verification_status.value,
                "notes": restaurant.verification_notes,
                "updated_at": restaurant.updated_at
            }
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update verification status: {str(e)}"
        )


@router.get("/restaurants/all", response_model=APIResponse)
def get_all_restaurants(
    status_filter: str = None,
    db: Session = Depends(get_db)
):
    """Get all restaurants with optional status filter (Admin only)"""
    query = db.query(Restaurant)
    
    if status_filter:
        try:
            status_enum = VerificationStatusEnum(status_filter)
            query = query.filter(Restaurant.verification_status == status_enum)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status filter: {status_filter}"
            )
    
    restaurants = query.all()
    
    restaurant_list = []
    for restaurant in restaurants:
        restaurant_list.append({
            "id": restaurant.id,
            "restaurant_name": restaurant.restaurant_name,
            "restaurant_type": restaurant.restaurant_type.value if restaurant.restaurant_type else None,
            "verification_status": restaurant.verification_status.value,
            "is_open": restaurant.is_open,
            "owner_phone": restaurant.owner.phone_number if restaurant.owner else None,
            "created_at": restaurant.created_at
        })
    
    return APIResponse(
        success=True,
        message=f"Found {len(restaurant_list)} restaurants",
        data={"restaurants": restaurant_list}
    )


# ============= Delivery Partner Admin APIs =============

@router.get("/delivery-partners/pending", response_model=APIResponse)
def get_pending_delivery_partners(db: Session = Depends(get_db)):
    """Get all delivery partners pending verification (Admin only)"""
    from app.models import DeliveryPartner
    
    delivery_partners = db.query(DeliveryPartner).filter(
        DeliveryPartner.verification_status.in_([
            VerificationStatusEnum.SUBMITTED,
            VerificationStatusEnum.UNDER_REVIEW
        ])
    ).all()
    
    partner_list = []
    for partner in delivery_partners:
        partner_list.append({
            "id": partner.id,
            "full_name": partner.full_name,
            "phone_number": partner.phone_number,
            "email": partner.email,
            "vehicle_number": partner.vehicle_number,
            "vehicle_type": partner.vehicle_type,
            "license_number": partner.license_number,
            "verification_status": partner.verification_status.value,
            "verification_notes": partner.verification_notes,
            "is_registered": partner.is_registered,
            "rating": float(partner.rating) if partner.rating else 5.0,
            "created_at": partner.created_at,
            "updated_at": partner.updated_at
        })
    
    return APIResponse(
        success=True,
        message=f"Found {len(partner_list)} delivery partners pending verification",
        data={"delivery_partners": partner_list}
    )


@router.get("/delivery-partners/{partner_id}/details", response_model=APIResponse)
def get_delivery_partner_verification_details(
    partner_id: int,
    db: Session = Depends(get_db)
):
    """Get detailed information for delivery partner verification (Admin only)"""
    from app.models import DeliveryPartner, Order
    
    partner = db.query(DeliveryPartner).filter(DeliveryPartner.id == partner_id).first()
    
    if not partner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Delivery partner not found"
        )
    
    # Get delivery statistics
    total_deliveries = db.query(Order).filter(
        Order.delivery_partner_id == partner_id,
        Order.status == "delivered"
    ).count()
    
    return APIResponse(
        success=True,
        message="Delivery partner details retrieved successfully",
        data={
            "partner": {
                "id": partner.id,
                "full_name": partner.full_name,
                "email": partner.email,
                "phone_number": partner.phone_number,
                "vehicle_number": partner.vehicle_number,
                "vehicle_type": partner.vehicle_type,
                "license_number": partner.license_number,
                "profile_photo": partner.profile_photo,
                "rating": float(partner.rating) if partner.rating else 5.0,
                "verification_status": partner.verification_status.value,
                "verification_notes": partner.verification_notes,
                "is_active": partner.is_active,
                "is_online": partner.is_online,
                "is_registered": partner.is_registered,
                "total_deliveries": total_deliveries,
                "created_at": partner.created_at,
                "updated_at": partner.updated_at,
                "last_online_at": partner.last_online_at,
                "last_offline_at": partner.last_offline_at
            }
        }
    )


@router.put("/delivery-partners/{partner_id}/verify", response_model=APIResponse)
async def update_delivery_partner_verification_status(
    partner_id: int,
    verification_data: UpdateVerificationRequest,
    db: Session = Depends(get_db)
):
    """Update delivery partner verification status (Admin only)"""
    from app.models import DeliveryPartner
    from app.services.notification_service import NotificationService
    
    try:
        # Validate status
        valid_statuses = ["under_review", "approved", "rejected"]
        if verification_data.status not in valid_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status. Must be one of: {valid_statuses}"
            )
        
        # Get delivery partner
        partner = db.query(DeliveryPartner).filter(DeliveryPartner.id == partner_id).first()
        
        if not partner:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Delivery partner not found"
            )
        
        # Convert string to enum
        status_enum = VerificationStatusEnum(verification_data.status)
        
        # Update status
        partner.verification_status = status_enum
        partner.verification_notes = verification_data.notes
        
        db.commit()
        db.refresh(partner)
        
        # Send notification to delivery partner
        notification_title = ""
        notification_message = ""
        
        if status_enum == VerificationStatusEnum.APPROVED:
            notification_title = "🎉 Registration Approved!"
            notification_message = "Congratulations! Your delivery partner registration has been approved. You can now go online and start accepting orders."
        elif status_enum == VerificationStatusEnum.REJECTED:
            notification_title = "Registration Rejected"
            notification_message = f"Sorry, your registration has been rejected. Reason: {verification_data.notes or 'Please contact support for details.'}"
        elif status_enum == VerificationStatusEnum.UNDER_REVIEW:
            notification_title = "Registration Under Review"
            notification_message = "Your registration is currently under review by our team. We'll notify you once it's completed."
        
        # Create notification
        await NotificationService.create_notification(
            db=db,
            delivery_partner_id=partner_id,
            title=notification_title,
            message=notification_message,
            notification_type="verification_update"
        )
        
        return APIResponse(
            success=True,
            message=f"Delivery partner verification status updated to {verification_data.status}",
            data={
                "partner_id": partner_id,
                "status": partner.verification_status.value,
                "notes": partner.verification_notes,
                "updated_at": partner.updated_at
            }
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update verification status: {str(e)}"
        )


@router.get("/delivery-partners/all", response_model=APIResponse)
def get_all_delivery_partners(
    status_filter: str = None,
    db: Session = Depends(get_db)
):
    """Get all delivery partners with optional status filter (Admin only)"""
    from app.models import DeliveryPartner
    
    query = db.query(DeliveryPartner)
    
    if status_filter:
        try:
            status_enum = VerificationStatusEnum(status_filter)
            query = query.filter(DeliveryPartner.verification_status == status_enum)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status filter: {status_filter}"
            )
    
    partners = query.all()
    
    partner_list = []
    for partner in partners:
        partner_list.append({
            "id": partner.id,
            "full_name": partner.full_name,
            "phone_number": partner.phone_number,
            "vehicle_type": partner.vehicle_type,
            "vehicle_number": partner.vehicle_number,
            "verification_status": partner.verification_status.value,
            "is_online": partner.is_online,
            "is_active": partner.is_active,
            "rating": float(partner.rating) if partner.rating else 5.0,
            "created_at": partner.created_at
        })
    
    return APIResponse(
        success=True,
        message=f"Found {len(partner_list)} delivery partners",
        data={"delivery_partners": partner_list}
    )
