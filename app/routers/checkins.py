from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.checkin import CheckIn
from app.models.database import get_db
from app.schemas.checkin_schema import CheckInCreate, CheckInOut
from app.services.anomaly_detection import detect_anomalies

router = APIRouter()


@router.get("/", response_model=List[CheckInOut])
def list_checkins(db: Session = Depends(get_db)):
    return db.query(CheckIn).order_by(CheckIn.created_at.desc()).all()


@router.post("/", response_model=CheckInOut)
def create_checkin(checkin: CheckInCreate, db: Session = Depends(get_db)):
    db_checkin = CheckIn(**checkin.model_dump())
    db.add(db_checkin)
    db.commit()
    db.refresh(db_checkin)
    return db_checkin


@router.get("/alerts")
def get_alerts(db: Session = Depends(get_db)):
    checkins = db.query(CheckIn).order_by(CheckIn.created_at.asc()).all()
    return detect_anomalies(checkins)