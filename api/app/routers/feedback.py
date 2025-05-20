from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.app.database_app import get_db
from api.app.crud import feedback as feedback_crud
from api.app.schemas.feedback import FeedbackCreate, FeedbackRead
from typing import List

router = APIRouter(prefix="/feedback", tags=["Feedback"])

@router.post("/feedback", response_model=FeedbackRead)
def create_feedback(
    feedback: FeedbackCreate,
    db: Session = Depends(get_db)
):
    db_feedback = feedback_crud.create_feedback(db=db, feedback=feedback)
    if not db_feedback:
        raise HTTPException(status_code=400, detail="Feedback could not be created")
    return db_feedback

@router.get("/professional/{professional_id}", response_model=List[FeedbackRead])
def list_feedback_by_professional(
    professional_id: int,
    db: Session = Depends(get_db)
):
    feedbacks = feedback_crud.get_feedback_by_professional(db=db, professional_id=professional_id)
    if not feedbacks:
        raise HTTPException(status_code=404, detail="No feedback found for this professional")
    return feedbacks

@router.get("/patient/{patient_id}", response_model=List[FeedbackRead])
def list_feedbacks_for_patient(patient_id: int, db: Session = Depends(get_db)):
    feedbacks = feedback_crud.get_feedback_by_patient(db=db, patient_id=patient_id)
    if not feedbacks:
        raise HTTPException(status_code=404, detail="No feedback found for this patient")
    return feedbacks

