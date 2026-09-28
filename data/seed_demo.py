import os
import random
from datetime import datetime, timedelta

os.environ["DATABASE_URL"] = "sqlite:///./demo.db"  # base dédiée à la démo

from app.models.checkin import CheckIn
from app.models.database import Base, SessionLocal, engine

Base.metadata.create_all(bind=engine)
db = SessionLocal()

random.seed(42)
now = datetime.utcnow()

# Humeur qui décline sur les derniers jours pour déclencher une alerte
moods = [4, 4, 5, 4, 3, 4, 3, 3, 2, 2]
sleeps = [4, 3, 4, 4, 3, 3, 2, 3, 2, 2]

for i, (m, s) in enumerate(zip(moods, sleeps)):
    db.add(CheckIn(
        created_at=now - timedelta(days=(len(moods) - i) * 2),
        person_label="Personne A (démo)",
        filled_by="proxy" if i % 2 == 0 else "self",
        mood_score=m,
        sleep_quality=s,
        medication_taken=random.choice(["yes", "yes", "partial"]) if i < 7 else "no",
    ))

db.commit()
print("Base de démo créée : demo.db")