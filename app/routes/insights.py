
from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Symptom
from app.services.insights import generate_insights

router = APIRouter(
    prefix="/api/insights",
    tags=["Insights"]
)


@router.get("/{patient_id}")
def get_patient_insights(
    patient_id: str,
    db: Session = Depends(get_db)
):
    if not patient_id.strip():
        raise HTTPException(
            status_code=400,
            detail="Patient ID cannot be empty."
        )

    today = date.today()
    start_date = today - timedelta(days=29)

    records = db.query(Symptom).filter(
        Symptom.patient_id == patient_id,
        Symptom.entry_date >= start_date,
        Symptom.entry_date <= today
    ).order_by(Symptom.entry_date.asc()).all()

    result = generate_insights(records)

    return {
        "patient_id": patient_id,
        "analysis_period": {
            "from": start_date,
            "to": today
        },
        **result
    }
