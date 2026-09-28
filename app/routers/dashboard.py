from pathlib import Path

from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.models.checkin import CheckIn
from app.models.database import get_db
from app.services.anomaly_detection import detect_anomalies

router = APIRouter()

templates_dir = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir))


@router.get("/dashboard")
def dashboard(request: Request, db: Session = Depends(get_db)):
    checkins = db.query(CheckIn).order_by(CheckIn.created_at.asc()).all()
    alerts = detect_anomalies(checkins)

    dates = [c.created_at.strftime("%d/%m") for c in checkins]
    mood_values = [c.mood_score for c in checkins]
    sleep_values = [c.sleep_quality for c in checkins]

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "checkins": list(reversed(checkins)),
            "alerts": alerts,
            "dates": dates,
            "mood_values": mood_values,
            "sleep_values": sleep_values,
        },
    )
@router.get("/simulator")
def simulator(request: Request):
    return templates.TemplateResponse("simulator.html", {"request": request})
@router.get("/checkin/new")
def new_checkin_form(request: Request):
    return templates.TemplateResponse("checkin_form.html", {"request": request})