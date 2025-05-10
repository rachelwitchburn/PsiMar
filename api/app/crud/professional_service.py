from sqlalchemy.orm import Session
from api.app.models.models import Professional, AccessCode
from api.app.schemas.user import UserCreate
from api.app.crud.user_crud import create_user
from fastapi import HTTPException


def create_psychologist(db: Session, user_data: UserCreate):
    # Validate access code
    access_code = db.query(AccessCode).filter_by(code=user_data.access_code).first()
    if not access_code or access_code.used:
        raise HTTPException(status_code=400, detail="Invalid or already used access code")

    # Create user (common functionality)
    user = create_user(db, user_data)

    # Create professional (psychologist) record
    professional = Professional(id=user.id, access_code=user_data.access_code)
    db.add(professional)

    # Mark the access code as used
    access_code.used = True

    # Commit transaction
    db.commit()
    db.refresh(user)
    db.refresh(professional)

    return professional

