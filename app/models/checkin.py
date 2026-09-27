from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.models.database import Base


class CheckIn(Base):
    """Un check-in = un point de suivi à un instant donné pour un proche."""

    __tablename__ = "checkins"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    person_label = Column(String, nullable=True)  # ex: "Maman", "Papa"
    filled_by = Column(String, nullable=False)  # "self" ou "proxy"

    mood_score = Column(Integer, nullable=True)  # 1-5
    sleep_quality = Column(Integer, nullable=True)  # 1-5
    pain_level = Column(Integer, nullable=True)  # 0-5
    medication_taken = Column(String, nullable=True)  # "yes" / "no" / "partial"

    had_appointment = Column(Boolean, nullable=True)
    appointment_note = Column(Text, nullable=True)
    free_notes = Column(Text, nullable=True)