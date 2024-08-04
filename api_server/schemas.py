# This file contains the Pydantic models.

from datetime import datetime
from pydantic import BaseModel
from typing_extensions import TypedDict

class DataPoint(TypedDict):
    x: float
    y: int

class DataPointList(BaseModel):
    data_point_list: list[DataPoint]

class DeviceList(BaseModel):
    device_list: list[str]

class TimeSeriesEntry(BaseModel):
    device_name: str
    vibration_velocity: int
    timestamp: datetime

class Token(BaseModel):
    access_token: str
    token_type: str
