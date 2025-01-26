from sqlalchemy import Column, Boolean, Integer, DateTime
from elevator.database.database import Base

class ElevatorDemand(Base):
    """
    ElevatorDemand model for DB transactions
    """
    __tablename__ = 'demand'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime)
    currentFloor = Column(Integer)
    requestedFloor = Column(Integer)
    isVacant = Column(Boolean)
    isWeekday = Column(Boolean)
    