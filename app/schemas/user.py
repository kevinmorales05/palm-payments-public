from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from typing import Optional


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
