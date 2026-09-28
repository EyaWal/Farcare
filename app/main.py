from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.models.database import Base, engine
from app.routers import checkins, dashboard, finance
from pathlib import Path
from fastapi.staticfiles import StaticFiles

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FarCare", description="Suivi et préparation pour les proches aidants à distance")
app.mount("/static", StaticFiles(directory=Path(__file__).resolve().parent / "static"), name="static")
app.include_router(checkins.router, prefix="/checkins", tags=["checkins"])
app.include_router(finance.router, prefix="/finance", tags=["finance"])
app.include_router(dashboard.router, tags=["dashboard"])




@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/dashboard")