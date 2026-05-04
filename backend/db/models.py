from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.sql import func
from db.database import Base

class ROI(Base):
    __tablename__ = "roi_data"

    id = Column(Integer, primary_key=True, index=True)
    frame_number = Column(Integer, nullable=False)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    width = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    confidence = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())