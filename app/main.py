from fastapi import FastAPI

from app.models.database import Base, engine
from app.routers import checkins, dashboard, finance

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FarCare", description="Suivi et préparation pour les proches aidants à distance")

app.include_router(checkins.router, prefix="/checkins", tags=["checkins"])
app.include_router(finance.router, prefix="/finance", tags=["finance"])
app.include_router(dashboard.router, tags=["dashboard"])


@app.get("/")
def root():
    return {"status": "FarCare API is running"}