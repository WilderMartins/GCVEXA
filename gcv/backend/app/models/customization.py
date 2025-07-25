from sqlalchemy import Column, Integer, String, Text
from ..db.base_class import Base

class Customization(Base):
    __tablename__ = "customization"

    id = Column(Integer, primary_key=True) # Usaremos sempre o id=1
    app_title = Column(String, default="GCV")
    logo_base64 = Column(Text, nullable=True)
