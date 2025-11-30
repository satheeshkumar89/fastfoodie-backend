import firebase_admin
from firebase_admin import credentials, auth
import os
from app.config import get_settings

settings = get_settings()


class FirebaseService:
    _initialized = False
    
    @classmethod
    def initialize(cls):
        """Initialize Firebase Admin SDK"""
        if cls._initialized:
            return
            
        try:
            # Check if service account key file exists
            service_account_path = os.getenv('FIREBASE_SERVICE_ACCOUNT_KEY', 'firebase-service-account.json')
            
            if os.path.exists(service_account_path):
                cred = credentials.Certificate(service_account_path)
                firebase_admin.initialize_app(cred)
                cls._initialized = True
                print("✓ Firebase Admin SDK initialized successfully")
            else:
                print(f"⚠ Firebase service account key not found at {service_account_path}")
                print("  Firebase OTP will be simulated in development mode")
        except Exception as e:
            print(f"⚠ Firebase initialization failed: {e}")
            print("  Firebase OTP will be simulated in development mode")
    
    @staticmethod
    def send_otp_via_firebase(phone_number: str) -> dict:
        """
        Send OTP via Firebase Authentication
        Returns session info for verification
        """
        try:
            # In a real implementation, Firebase handles OTP on the client side
            # The backend just verifies the token
            # This is a placeholder for the flow
            
            if not FirebaseService._initialized:
                # Development mode - simulate OTP
                import random
                otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
                print(f"\n{'='*50}")
                print(f"📱 DEVELOPMENT MODE - OTP for {phone_number}: {otp}")
                print(f"{'='*50}\n")
                return {
                    "success": True,
                    "mode": "development",
                    "otp": otp,  # Only in development
                    "message": "OTP sent (development mode)"
                }
            
            # Production mode with Firebase
            # Note: Firebase Auth typically handles OTP on client side
            # Backend receives the ID token for verification
            return {
                "success": True,
                "mode": "production",
                "message": "OTP sent via Firebase"
            }
            
        except Exception as e:
            print(f"Error sending Firebase OTP: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def verify_firebase_token(id_token: str) -> dict:
        """
        Verify Firebase ID token
        Returns decoded token with user info
        """
        try:
            if not FirebaseService._initialized:
                # Development mode - skip verification
                return {
                    "success": True,
                    "mode": "development",
                    "uid": "dev_user_123",
                    "phone_number": "+1234567890"
                }
            
            # Verify the ID token
            decoded_token = auth.verify_id_token(id_token)
            return {
                "success": True,
                "mode": "production",
                "uid": decoded_token.get('uid'),
                "phone_number": decoded_token.get('phone_number'),
                "email": decoded_token.get('email')
            }
            
        except Exception as e:
            print(f"Error verifying Firebase token: {e}")
            return {
                "success": False,
                "error": str(e)
            }


# Initialize Firebase on module import
FirebaseService.initialize()
