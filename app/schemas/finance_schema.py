from pydantic import BaseModel, Field


class SimulationInput(BaseModel):
    initial_savings: float = Field(2000, ge=0, description="Épargne de départ (EUR)")
    monthly_contribution: float = Field(150, ge=0, description="Épargne mensuelle (EUR)")
    horizon_years: int = Field(10, ge=1, le=30)
    annual_event_probability: float = Field(0.15, ge=0, le=1)
    median_event_cost: float = Field(3000, gt=0, description="Coût médian d'un événement (EUR)")
    cost_sigma: float = Field(0.8, gt=0, le=2, description="Dispersion des coûts (log-normale)")
    fx_volatility: float = Field(0.10, ge=0, le=1, description="Volatilité du taux de change")
    n_simulations: int = Field(5000, ge=100, le=50000)
    confidence: float = Field(0.90, gt=0, lt=1)