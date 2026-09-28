from fastapi import APIRouter

from app.schemas.finance_schema import SimulationInput
from app.services.monte_carlo import run_monte_carlo_simulation

router = APIRouter()


@router.post("/simulate")
def run_simulation(params: SimulationInput):
    return run_monte_carlo_simulation(**params.model_dump())