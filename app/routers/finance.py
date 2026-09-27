from fastapi import APIRouter

router = APIRouter()


@router.post("/simulate")
def run_simulation():
    """Placeholder — appellera app.services.monte_carlo une fois le modèle financier défini."""
    return {"message": "endpoint à implémenter"}
