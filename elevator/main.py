from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, load_only
from datetime import datetime
from elevator.models.models import ElevatorDemand
from elevator.schemas import schemas
from elevator.database.database import engine, get_db, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/health")
async def check_health():
    return "OK"

@app.post('/demand', response_model=schemas.ElevatorDemandResponseSchema)
async def add_demand(request: schemas.ElevatorDemandSchema, db: Session = Depends(get_db)):

    if request.requestedFloor < -2: # assuming there are 2 basement floors
        raise HTTPException(status_code=400, detail="Invalid floor number")
    
    last_demand = db.query(ElevatorDemand).order_by(ElevatorDemand.id.desc()).first()
    
    if last_demand is not None:

        demand = ElevatorDemand(
            timestamp = datetime.utcnow(),
            currentFloor = last_demand.requestedFloor,
            requestedFloor = request.requestedFloor,
            isVacant = request.isVacant,
            isWeekday = datetime.utcnow().weekday() < 5 # the weekday method returns 5 and 6 for saturday and sunday
        )

    else:
        demand = ElevatorDemand(
            timestamp = datetime.utcnow(),
            currentFloor = 0,
            requestedFloor = request.requestedFloor,
            isVacant = request.isVacant,
            isWeekday = datetime.utcnow().weekday() < 5 # the weekday method returns 5 and 6 for saturday and sunday
        )
        
    db.add(demand)
    db.commit()
    db.refresh(demand)

    
    return demand

@app.get("/demand", response_model=schemas.ElevatorDemandHistory)
async def get_demand_history(db: Session = Depends(get_db)):
    try:
        history = db.query(ElevatorDemand).all()

        return {"data": history}
    except Exception as e:
        return {"error": e}
