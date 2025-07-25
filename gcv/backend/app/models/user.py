from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from ..db.base_class import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)

    mfa_secret = Column(String, nullable=True)
    mfa_enabled = Column(Boolean(), default=False)

    # Relações centralizadas
    assets = relationship("Asset", back_populates="owner", cascade="all, delete-orphan")
    scans = relationship("Scan", back_populates="user", cascade="all, delete-orphan")
    events = relationship("VulnerabilityEvent", back_populates="user")
    roles = relationship("Role", secondary="user_roles", back_populates="users")
