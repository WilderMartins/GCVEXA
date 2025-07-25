from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from app.db.base_class import Base

class Collector(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    tool = Column(String)
    collector_type = Column(String)
    config = Column(JSONB)
