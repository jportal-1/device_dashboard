# This file contains the SQLAlchemy models.

from .database import Base
from sqlalchemy import Column, DateTime, Integer, String


class TimeSeriesEntryDB(Base):

    __tablename__ = "timeseries"
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    device_name = Column(String(length=128), nullable=False, index=True)
    vibration_velocity = Column(Integer, nullable=False)

class UserEntryDB(Base):

    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(length=128), nullable=False, index=True)
    hashed_password = Column(String(length=128), nullable=False)