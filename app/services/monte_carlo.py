from typing import Optional

import numpy as np


def run_monte_carlo_simulation(
    initial_savings: float,
    monthly_contribution: float,
    horizon_years: int = 10,
    annual_event_probability: float = 0.15,
    median_event_cost: float = 3000.0,
    cost_sigma: float = 0.8,
    fx_volatility: float = 0.10,
    n_simulations: int = 5000,
    confidence: float = 0.90,
    seed: Optional[int] = None,
) -> dict:
    """
    Simule des chocs de dépenses de santé imprévues à l'international.

    - Un événement peut survenir chaque mois (probabilité dérivée de la probabilité annuelle)
    - Son coût suit une loi log-normale (médiane + dispersion)
    - Un facteur de change aléatoire (log-normal) amplifie ou réduit le coût en EUR
    """
    rng = np.random.default_rng(seed)
    n_months = horizon_years * 12
    shape = (n_simulations, n_months)

    monthly_p = 1 - (1 - annual_event_probability) ** (1 / 12)

    events = rng.random(shape) < monthly_p
    costs = rng.lognormal(mean=np.log(median_event_cost), sigma=cost_sigma, size=shape)
    fx_factor = rng.lognormal(mean=0.0, sigma=fx_volatility, size=shape)
    shocks = events * costs * fx_factor

    net_flow = monthly_contribution - shocks
    balance = initial_savings + np.cumsum(net_flow, axis=1)

    # Probabilité de passer sous zéro à un moment de l'horizon
    shortfall_probability = float(np.mean(balance.min(axis=1) < 0))

    # Fonds initial nécessaire pour ne jamais passer sous zéro, scénario par scénario
    required_fund = np.maximum(0, (-np.cumsum(net_flow, axis=1)).max(axis=1))
    recommended_fund = float(np.quantile(required_fund, confidence))

    final_balance = balance[:, -1]

    # Trajectoires annuelles (p10 / p50 / p90) pour un futur fan chart
    year_idx = [12 * y - 1 for y in range(1, horizon_years + 1)]
    yearly = balance[:, year_idx]
    fan_chart = {
        "years": list(range(1, horizon_years + 1)),
        "p10": np.percentile(yearly, 10, axis=0).round(0).tolist(),
        "p50": np.percentile(yearly, 50, axis=0).round(0).tolist(),
        "p90": np.percentile(yearly, 90, axis=0).round(0).tolist(),
    }

    return {
        "shortfall_probability": round(shortfall_probability, 4),
        "recommended_fund": round(recommended_fund, 0),
        "confidence": confidence,
        "final_balance": {
            "p10": round(float(np.percentile(final_balance, 10)), 0),
            "p50": round(float(np.percentile(final_balance, 50)), 0),
            "p90": round(float(np.percentile(final_balance, 90)), 0),
        },
        "avg_events_over_horizon": round(float(events.sum(axis=1).mean()), 2),
        "fan_chart": fan_chart,
    }