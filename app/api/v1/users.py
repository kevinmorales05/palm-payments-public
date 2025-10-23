from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
from app.db.session import SessionLocal
from app.models.user import User, UserBiometrics
from app.schemas.user import (
    UserRead,
    UserCreate,
    UserResponse,
    UserBiometricCreate,
)

from app.core.security import get_password_hash  # assumes you have password hashing util

router = APIRouter(prefix="/users", tags=["Users"])


# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --------------------------------------------------------------------
# Read users
# --------------------------------------------------------------------
@router.get("/", response_model=list[UserRead])
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


# --------------------------------------------------------------------
# STEP 1: Create basic user (registration)
# --------------------------------------------------------------------
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    print("Password repr:", repr(user.password))
    print("Length (chars):", len(user.password))
    print("Length (bytes):", len(user.password.encode("utf-8")))
    hashed_password = get_password_hash(user.password)
    print(hashed_password)

    new_user = User(
        email=user.email,
        name=user.name,
        last_name=user.last_name,
        password=hashed_password,
        identification_number=user.identification_number,
        id_type=user.id_type,
        country_code=user.country_code,
        telephone=user.telephone,
        enrol_ts=int(datetime.utcnow().timestamp()),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserResponse(
        user_id=new_user.user_id,
        email=new_user.email,
        name=new_user.name,
        last_name=new_user.last_name,
        status=new_user.status,
        biometrics_registered=False,
    )


# --------------------------------------------------------------------
# STEP 2: Register biometrics (optional second phase)
# --------------------------------------------------------------------
@router.post("/biometrics", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_biometrics(bio: UserBiometricCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == bio.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Prevent duplicate biometric registration
    existing_bio = db.query(UserBiometrics).filter(UserBiometrics.user_id == bio.user_id).first()
    if existing_bio:
        raise HTTPException(status_code=400, detail="Biometrics already registered for this user")

    biometrics = UserBiometrics(
        user_id=bio.user_id,
        public_key=bio.public_key,
        encrypted_protected_template=bio.encrypted_protected_template,
        template_meta=bio.template_meta,
        consent_record_biometrics=bio.consent_record_biometrics,
        device_policy_biometrics=bio.device_policy_biometrics,
        enrol_ts_biometric=bio.enrol_ts_biometric or int(datetime.utcnow().timestamp()),
    )

    db.add(biometrics)
    db.commit()
    db.refresh(biometrics)

    return UserResponse(
        user_id=user.user_id,
        email=user.email,
        name=user.name,
        last_name=user.last_name,
        status=user.status,
        biometrics_registered=True,
    )
