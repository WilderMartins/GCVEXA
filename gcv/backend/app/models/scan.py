from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..db.base_class import Base
import datetime

class Scan(Base):
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)

    gvm_task_id = Column(String, unique=True, index=True, nullable=True)
    status = Column(String, default="Requested") # Ex: Requested, Running, Done, Failed
    started_at = Column(DateTime, default=datetime.datetime.utcnow)

    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    asset = relationship("Asset", back_populates="scans")

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="scans")

    config_id = Column(Integer, ForeignKey("scanner_configs.id"))
    config = relationship("ScannerConfig")