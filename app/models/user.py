import uuid
from sqlalchemy import Column, String, ForeignKey, Integer, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base  # <-- import the shared Base



class User(Base):
    __tablename__ = "users"

    # Primary key
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)

    # Basic registration info
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    password = Column(String, nullable=False)
    identification_number = Column(String, nullable=False)
    id_type = Column(String, nullable=False)
    country_code = Column(String, nullable=False)
    telephone = Column(String, nullable=False)
    status = Column(String, nullable=False, default="active")

    # Consent and policy management (first-step data)
    consent_record = Column(String, nullable=False, default="pending")
    device_policy = Column(String, nullable=False, default="pending")
    enrol_ts = Column(Integer, nullable=True)       # epoch timestamp
    last_auth_ts = Column(Integer, nullable=True)
    audit_log_id = Column(String, nullable=True)

    # Relationship with biometrics
    biometrics = relationship("UserBiometrics", back_populates="user", uselist=False)


class UserBiometrics(Base):
    __tablename__ = "user_biometrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False, unique=True)

    # Biometric data (optional second-step fields)
    public_key = Column(String, nullable=False)
    encrypted_protected_template = Column(String, nullable=False)
    template_meta = Column(String, nullable=False)
    consent_record_biometrics = Column(String, nullable=False, default="pending")
    device_policy_biometrics = Column(String, nullable=False, default="pending")
    enrol_ts_biometric = Column(Integer, nullable=True)

    user = relationship("User", back_populates="biometrics")
