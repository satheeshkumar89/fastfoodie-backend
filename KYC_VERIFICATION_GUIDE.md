# 🔐 KYC Verification Flow - Complete Guide

## 📋 Overview

The KYC (Know Your Customer) verification process has **two sides**:
1. **Restaurant Owner** - Submits KYC documents
2. **Admin** - Reviews and approves/rejects KYC

---

## 🏪 Restaurant Owner Flow

### Step 1: Complete Restaurant Setup
```
1. Create restaurant details
2. Add restaurant address
3. Upload required documents
```

### Step 2: Upload Documents
```
Required Documents:
- FSSAI License (mandatory)
- Restaurant Photo (mandatory)
```

**Upload Process:**
```
1. GET presigned URL
2. Upload file to S3
3. Confirm upload
```

### Step 3: Submit for KYC
```
POST /restaurant/submit-kyc
```

**What happens:**
- Status changes: `pending` → `submitted`
- Admin is notified (in production)
- Restaurant waits for review

**Response:**
```json
{
  "success": true,
  "message": "KYC submitted successfully. Your restaurant will be reviewed shortly.",
  "data": {
    "status": "submitted"
  }
}
```

### Step 4: Check Verification Status
```
GET /restaurant/verification-status
```

**Response:**
```json
{
  "success": true,
  "data": {
    "status": "submitted",  // or "under_review", "approved", "rejected"
    "verification_notes": null,
    "updated_at": "2025-11-24T21:00:00Z"
  }
}
```

---

## 👨‍💼 Admin Flow (NEW ENDPOINTS)

### 1. Get Pending Restaurants
```
GET /admin/restaurants/pending
```

**Returns:** All restaurants with status `submitted` or `under_review`

**Response:**
```json
{
  "success": true,
  "message": "Found 5 restaurants pending verification",
  "data": {
    "restaurants": [
      {
        "id": 1,
        "restaurant_name": "Tasty Bites",
        "restaurant_type": "restaurant",
        "fssai_license_number": "12345678901234",
        "verification_status": "submitted",
        "verification_notes": null,
        "owner_name": "John Doe",
        "owner_phone": "+918668198712",
        "created_at": "2025-11-24T20:00:00Z",
        "updated_at": "2025-11-24T20:30:00Z"
      }
    ]
  }
}
```

### 2. Get Restaurant Details for Review
```
GET /admin/restaurants/{restaurant_id}/details
```

**Returns:** Complete restaurant information including documents

**Response:**
```json
{
  "success": true,
  "data": {
    "restaurant": {
      "id": 1,
      "restaurant_name": "Tasty Bites",
      "fssai_license_number": "12345678901234",
      "verification_status": "submitted",
      "opening_time": "09:00",
      "closing_time": "22:00"
    },
    "owner": {
      "full_name": "John Doe",
      "email": "john@example.com",
      "phone_number": "+918668198712"
    },
    "address": {
      "address_line_1": "123 Main Street",
      "city": "Bangalore",
      "state": "Karnataka",
      "pincode": "560001"
    },
    "cuisines": ["Indian", "Chinese"],
    "documents": [
      {
        "document_type": "fssai_license",
        "file_url": "https://s3.../fssai_license.pdf",
        "file_name": "license.pdf",
        "uploaded_at": "2025-11-24T20:00:00Z"
      },
      {
        "document_type": "restaurant_photo",
        "file_url": "https://s3.../restaurant.jpg",
        "file_name": "photo.jpg",
        "uploaded_at": "2025-11-24T20:05:00Z"
      }
    ]
  }
}
```

### 3. Update Verification Status ⭐
```
PUT /admin/restaurants/{restaurant_id}/verify
```

**Request Body:**
```json
{
  "status": "approved",  // or "rejected" or "under_review"
  "notes": "All documents verified successfully"
}
```

**Valid Statuses:**
- `under_review` - Admin is reviewing
- `approved` - KYC approved ✅
- `rejected` - KYC rejected ❌

**Response:**
```json
{
  "success": true,
  "message": "Restaurant verification status updated to approved",
  "data": {
    "restaurant_id": 1,
    "status": "approved",
    "notes": "All documents verified successfully",
    "updated_at": "2025-11-24T21:00:00Z"
  }
}
```

### 4. Get All Restaurants (with filter)
```
GET /admin/restaurants/all?status_filter=approved
```

**Optional Query Param:**
- `status_filter`: pending, submitted, under_review, approved, rejected

---

## 🔄 Complete KYC Workflow

```
Restaurant Owner                    Admin
       |                              |
       |-- Create Restaurant          |
       |-- Upload Documents           |
       |-- Submit KYC --------------->|
       |                              |
       |                              |-- Get Pending List
       |                              |-- View Details
       |                              |-- Review Documents
       |                              |
       |<-- Status: under_review -----|
       |                              |
       |                              |-- Approve/Reject
       |<-- Status: approved ---------|
       |                              |
       |-- Check Status               |
       |-- Restaurant is LIVE! 🎉     |
```

---

## 📊 Verification Status Flow

```
pending (initial)
   ↓
submitted (after submit-kyc)
   ↓
under_review (admin reviewing)
   ↓
approved ✅  OR  rejected ❌
```

---

## 🎯 Example: Admin Approving KYC

### Step 1: Get Pending Restaurants
```bash
GET /admin/restaurants/pending
```

### Step 2: View Restaurant Details
```bash
GET /admin/restaurants/1/details
```

### Step 3: Review Documents
- Check FSSAI license PDF
- Verify restaurant photo
- Validate address

### Step 4: Approve
```bash
PUT /admin/restaurants/1/verify
Body: {
  "status": "approved",
  "notes": "All documents verified. FSSAI license valid."
}
```

### Step 5: Restaurant is Live!
- Owner can now accept orders
- Restaurant appears in customer app

---

## 🎯 Example: Admin Rejecting KYC

```bash
PUT /admin/restaurants/1/verify
Body: {
  "status": "rejected",
  "notes": "FSSAI license expired. Please upload valid license."
}
```

**Owner sees:**
```json
{
  "status": "rejected",
  "verification_notes": "FSSAI license expired. Please upload valid license."
}
```

**Owner can:**
1. Upload new documents
2. Submit KYC again

---

## 🔑 Key Points

1. **Restaurant submits** → Status becomes `submitted`
2. **Admin reviews** → Status becomes `under_review`
3. **Admin approves** → Status becomes `approved` ✅
4. **Admin rejects** → Status becomes `rejected` ❌
5. **Owner can resubmit** if rejected

---

## 🚀 API Endpoints Summary

### Restaurant Owner:
- `POST /restaurant/submit-kyc` - Submit for verification
- `GET /restaurant/verification-status` - Check status

### Admin:
- `GET /admin/restaurants/pending` - Get pending list
- `GET /admin/restaurants/{id}/details` - View details
- `PUT /admin/restaurants/{id}/verify` - Approve/Reject
- `GET /admin/restaurants/all` - Get all restaurants

---

## 🔐 Security Note

In production, admin endpoints should be protected with:
- Admin authentication
- Role-based access control (RBAC)
- Audit logging

For now, these endpoints are accessible with any valid token. You should add admin-only middleware later.

---

## ✅ Testing Flow

1. **As Restaurant Owner:**
   ```
   - Create restaurant
   - Upload documents
   - Submit KYC
   - Check status
   ```

2. **As Admin:**
   ```
   - Get pending restaurants
   - View restaurant details
   - Approve or reject
   ```

3. **As Restaurant Owner:**
   ```
   - Check status again
   - See approval/rejection
   ```

---

**Your KYC verification system is now complete!** 🎉
