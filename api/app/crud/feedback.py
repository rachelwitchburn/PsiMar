from sqlalchemy.orm import Session
from api.app.models.models import Feedback
from api.app.schemas.feedback import FeedbackCreate


def create_feedback(db: Session, feedback: FeedbackCreate):
    db_feedback = Feedback(**feedback.dict())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

def get_feedback_by_professional_id(db: Session, professional_id: int):
    return db.query(Feedback).filter(Feedback.professional_id == professional_id).order_by(Feedback.date.desc()).all()

def get_feedback_by_patient(db: Session, patient_id: int):
    return db.query(Feedback).filter(Feedback.patient_id == patient_id).order_by(Feedback.date.desc()).all()