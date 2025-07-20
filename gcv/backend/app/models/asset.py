from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..db.base_class import Base

class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    type = Column(String, nullable=False) # e.g., "host", "application", "repository"
    address = Column(String, nullable=False, unique=True) # e.g., IP, URL do repo, URL da app

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="assets")

    scans = relationship("Scan", back_populates="asset")

# Adicionar a relação inversa no modelo User
from .user import User
User.assets = relationship("Asset", order_by=Asset.id, back_populates="owner")
