from sqlalchemy import Column, Integer, String
from ..db.base_class import Base

class ScannerConfig(Base):
    __tablename__ = "scanner_configs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False) # Ex: "OpenVAS Principal"
    url = Column(String, nullable=False)
    username = Column(String, nullable=False)
    encrypted_password = Column(String, nullable=False)
    type = Column(String, default="openvas") # Para futuras integrações
