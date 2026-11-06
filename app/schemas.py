
from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict, field_validator


class SymptomCreate(BaseModel):

    patient_id: str = Field(min_length=1, max_length=100)

    symptom: str = Field(min_length=1, max_length=200)

    severity: int = Field(ge=1, le=10)

    duration_hours: float = Field(gt=0, le=168)

    entry_date: date = Field(default_factory=date.today)

    possible_trigger: Optional[str] = None

    notes: Optional[str] = None

    @field_validator("patient_id", "symptom")
    @classmethod
    def validate_required_text(cls, value):
        if not value.strip():
            raise ValueError("This field cannot be empty")
        return value.strip()

    @field_validator("possible_trigger", "notes")
    @classmethod
    def clean_optional_text(cls, value):
        if value is not None:
            value = value.strip()
            return value or None
        return value


class SymptomResponse(BaseModel):

    id: int
    patient_id: str
    symptom: str
    severity: int
    duration_hours: float
    entry_date: date
    possible_trigger: Optional[str] = None
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
