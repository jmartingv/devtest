from pydantic import BaseModel
from datetime import datetime
from typing import List

class ElevatorDemandSchema(BaseModel):
    """Schema used for POST requests addin new elevator demands"""
    requestedFloor: int
    isVacant: bool

class ElevatorDemandResponseSchema(BaseModel):
    """
    Schema used for the API responses with single entries
    """
    id: int
    timestamp: datetime
    currentFloor: int
    requestedFloor: int
    isVacant: bool
    isWeekday: bool

class ElevatorDemandHistory(BaseModel):
    """Schema used for returning a list of demand entries (history) """
    data: List[ElevatorDemandResponseSchema]
    