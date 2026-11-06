
from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models import Symptom
from app.schemas import SymptomCreate, SymptomResponse

router = APIRouter(
    prefix="/api/symptoms",
    tags=["Symptoms"]
)


@router.post(
    "",
    response_model=SymptomResponse,
    status_code=status.HTTP_201_CREATED
)
def create_symptom(
    symptom_data: SymptomCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(Symptom).filter(
        Symptom.patient_id == symptom_data.patient_id,
        Symptom.symptom == symptom_data.symptom,
        Symptom.entry_date == symptom_data.entry_date
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="This symptom has already been logged for this date."
        )

    new_symptom = Symptom(**symptom_data.model_dump())

    try:
        db.add(new_symptom)
        db.commit()
        db.refresh(new_symptom)
        return new_symptom

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Duplicate symptom entry detected."
        )


@router.get("/{patient_id}/weekly", response_model=list[SymptomResponse])
def get_weekly_history(
    patient_id: str,
    db: Session = Depends(get_db)
):
    today = date.today()
    start_date = today - timedelta(days=6)

    symptoms = db.query(Symptom).filter(
        Symptom.patient_id == patient_id,
        Symptom.entry_date >= start_date,
        Symptom.entry_date <= today
    ).order_by(Symptom.entry_date.desc()).all()

    return symptoms


@router.get("/{patient_id}", response_model=list[SymptomResponse])
def get_all_history(
    patient_id: str,
    db: Session = Depends(get_db)
):
    return db.query(Symptom).filter(
        Symptom.patient_id == patient_id
    ).order_by(Symptom.entry_date.desc()).all()
