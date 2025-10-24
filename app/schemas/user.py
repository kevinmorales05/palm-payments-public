from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from typing import List, Optional


# ----------------------------
# Base Schema
# ----------------------------
class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    last_name: Optional[str] = None
    identification_number: Optional[str] = None
    id_type: Optional[str] = None
    country_code: Optional[str] = None
    telephone: Optional[str] = None
    status: Optional[str] = "active"
    consent_record: Optional[str] = "pending"
    device_policy: Optional[str] = "pending"

    model_config = {
        "from_attributes": True  # replaces orm_mode=True in Pydantic v2
    }


# ----------------------------
# Create User (Step 1)
# ----------------------------
class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


# ----------------------------
# Biometrics (Step 2)
# ----------------------------
class UserBiometricCreate(BaseModel):
    user_id: UUID
    public_key: str
    encrypted_protected_template: str
    template_meta: str
    consent_record_biometrics: Optional[str] = "pending"
    device_policy_biometrics: Optional[str] = "pending"
    enrol_ts_biometric: Optional[int] = None

    model_config = {
        "from_attributes": True
    }

# ----------------------------
# Image Model 
# ----------------------------

class BiometricImage(BaseModel):
    """Represents one palm image in base64 format."""
    image_id: Optional[str] = Field(None, description="Optional image identifier for tracking or debugging")
    image_base64: str = Field(..., description="Base64-encoded palm image")
    hand: Optional[str] = Field(None, description="Which hand: 'left' or 'right'")
    position: Optional[str] = Field(None, description="Optional capture angle or position info")

# ----------------------------
# User Images Schema 
# ----------------------------

class UserBiometricImagesCreate(BaseModel):
    """Request DTO for creating or enrolling palm biometrics."""
    user_id: UUID
    consent_record_biometrics: Optional[str] = Field("pending", description="User consent status for biometric use")
    device_policy_biometrics: Optional[str] = Field("pending", description="User device policy acceptance status")
    enrol_ts_biometric: Optional[int] = Field(None, description="Enrollment timestamp or tracking token")
    images: List[BiometricImage] = Field(..., description="List of biometric palm images in base64 format")

    model_config = {
        "from_attributes": True
    }

# ----------------------------
# Response schemas
# ----------------------------
class UserRead(BaseModel):
    user_id: UUID
    email: EmailStr
    name: Optional[str] = None
    last_name: Optional[str] = None
    status: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


class UserResponse(BaseModel):
    user_id: UUID
    email: EmailStr
    name: Optional[str] = None
    last_name: Optional[str] = None
    status: Optional[str] = None
    biometrics_registered: bool = False

    model_config = {
        "from_attributes": True
    }
