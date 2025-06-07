from sqlalchemy.orm import Session
from api.app.models.models import Feedback, Patient, Professional
from api.app.schemas.feedback import FeedbackCreate
from api.app.logger_config import logging

logger = logging.getLogger(__name__)

def create_feedback(db: Session, feedback: FeedbackCreate):
    # Validação de existência do paciente
    patient = db.query(Patient).filter(Patient.id == feedback.patient_id).first()
    if not patient:
        logger.warning(f"Tentativa de criar feedback com patient_id inválido: {feedback.patient_id}")
        raise ValueError(f"Paciente com o id {feedback.patient_id} não existe.")

    # Validação de existência do profissional
    professional = db.query(Professional).filter(Professional.id == feedback.professional_id).first()
    if not professional:
        logger.warning(f"Tentativa de criar feedback com professional_id inválido: {feedback.professional_id}")
        raise ValueError(f"Profissional com id {feedback.professional_id} não existe.")

    new_feedback = Feedback(
        message=feedback.message,
        patient_id=feedback.patient_id,
        professional_id=feedback.professional_id
    )
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)

    logger.info(f"Feedback criado com sucesso: {new_feedback.id}")
    return new_feedback

def get_feedback_by_professional_id(db: Session, professional_id: int):
    feedbacks = db.query(Feedback).filter(
        Feedback.professional_id == professional_id
    ).order_by(Feedback.date.desc()).all()

    logger.info(f"Consulta de feedbacks para profissional {professional_id}: {len(feedbacks)} encontrados")
    return feedbacks

def get_feedback_by_patient(db: Session, patient_id: int):
    feedbacks = db.query(Feedback).filter(
        Feedback.patient_id == patient_id
    ).order_by(Feedback.date.desc()).all()

    logger.info(f"Consulta de feedbacks para paciente {patient_id}: {len(feedbacks)} encontrados")
    return feedbacks