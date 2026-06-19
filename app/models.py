from sqlalchemy import Column, Integer, String, Float, DateTime  # ← DateTime, а не DATETIME
from app.database import Base
from sqlalchemy.sql import func

class Dinosaur(Base):
    __tablename__ = "dinosaurs"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    period = Column(String(50))
    length_min = Column(Float)
    length_max = Column(Float)
    weight_min = Column(Float)
    weight_max = Column(Float)
    image_url = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())  # ← DateTime
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
