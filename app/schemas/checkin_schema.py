from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CheckInCreate(BaseModel):
    person_label: Optional[str] = None
    filled_by: str = Field(..., pattern="^(self|proxy)$")
    mood_score: Optional[int] = Field(None, ge=1, le=5)
    sleep_quality: Optional[int] = Field(None, ge=1, le=5)
    pain_level: Optional[int] = Field(None, ge=0, le=5)
    medication_taken: Optional[str] = Field(None, pattern="^(yes|no|partial)$")
    had_appointment: Optional[bool] = None
    appointment_note: Optional[str] = None
    free_notes: Optional[str] = None


class CheckInOut(CheckInCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True