
from sqlalchemy import Column, Integer, String, Float, Date, Text, UniqueConstraint, CheckConstraint
from app.database import Base
class Symptom(Base):
    __tablename__ = "symptoms"
    __table_args__ = (
        UniqueConstraint(
            "patient_id",
            "symptom",
            "entry_date",
            name="unique_patient_symptom_date"
        ),
        CheckConstraint(
            "severity >= 1 AND severity <= 10",
            name="valid_severity"
        ),
        CheckConstraint(
            "duration_hours > 0",
            name="valid_duration"
        ),
    )
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String(100), nullable=False, index=True)
    symptom = Column(String(200), nullable=False)
    severity = Column(Integer, nullable=False)
    duration_hours = Column(Float, nullable=False)
    entry_date = Column(Date, nullable=False, index=True)
    possible_trigger = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
