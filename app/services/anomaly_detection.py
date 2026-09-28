from datetime import datetime, timedelta
from typing import List


def detect_anomalies(checkins: List, silence_threshold_days: int = 4, lookback: int = 5) -> List[dict]:
    """
    Analyse une liste de check-ins (triée du plus ancien au plus récent) et retourne
    une liste d'alertes détectées.
    """
    alerts = []

    if not checkins:
        return alerts

    # --- 1. Silence prolongé ---
    last_checkin = checkins[-1]
    days_since_last = (datetime.utcnow() - last_checkin.created_at).days
    if days_since_last >= silence_threshold_days:
        alerts.append({
            "type": "silence",
            "severity": "warning",
            "message": f"Aucun check-in depuis {days_since_last} jours (dernier : {last_checkin.created_at.strftime('%d/%m')}).",
        })

    recent = checkins[-lookback:]

    # --- 2. Médicament manqué de façon répétée ---
    med_values = [c.medication_taken for c in recent if c.medication_taken is not None]
    missed = [v for v in med_values if v in ("no", "partial")]
    if len(med_values) >= 3 and len(missed) / len(med_values) >= 0.5:
        alerts.append({
            "type": "medication",
            "severity": "warning",
            "message": f"Médicament non pris correctement sur {len(missed)}/{len(med_values)} des derniers check-ins.",
        })

    # --- 3. Tendance à la baisse (humeur) ---
    mood_values = [c.mood_score for c in recent if c.mood_score is not None]
    if len(mood_values) >= 3 and _is_declining(mood_values):
        alerts.append({
            "type": "mood_decline",
            "severity": "info",
            "message": f"L'humeur semble en baisse sur les derniers check-ins ({mood_values}).",
        })

    # --- 3bis. Tendance à la baisse (sommeil) ---
    sleep_values = [c.sleep_quality for c in recent if c.sleep_quality is not None]
    if len(sleep_values) >= 3 and _is_declining(sleep_values):
        alerts.append({
            "type": "sleep_decline",
            "severity": "info",
            "message": f"La qualité du sommeil semble en baisse sur les derniers check-ins ({sleep_values}).",
        })

    return alerts


def _is_declining(values: List[int]) -> bool:
    """Heuristique simple : la valeur baisse (ou stagne bas) sur au moins 3 points consécutifs."""
    diffs = [values[i + 1] - values[i] for i in range(len(values) - 1)]
    return sum(1 for d in diffs if d < 0) >= len(diffs) * 0.5