import logging

from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from api.app.models.models import User, Patient, Professional, AccessCode
from api.app.schemas.user import UserCreate, UserTypeEnum

logger = logging.getLogger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user: UserCreate):
    logger.info(f"Tentando criar usuário com e-mail: {user.email}")

    user_exists = db.query(User).filter_by(email=user.email).first()
    if user_exists:
        logger.warning(f"E-mail já registrado: {user.email}")
        raise HTTPException(status_code=400, detail="Email já cadastrado.")

    hashed_password = pwd_context.hash(user.password)

    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=str(user.email),
        password=hashed_password,
        user_type=user.user_type
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    logger.info(f"Usuário criado com ID {db_user.id} e tipo {user.user_type}")

    if user.user_type == UserTypeEnum.professional:
        logger.info(f"Validando código de acesso para profissional: {user.access_code}")
        code = db.query(AccessCode).filter_by(code=user.access_code).first()
        if not code or code.used:
            logger.error("Código de acesso inválido ou já utilizado.")
            raise HTTPException(status_code=400, detail="Código de acesso inválido ou já utilizado.")

        professional = Professional(
            id=db_user.id,
            access_code=user.access_code
        )
        db.add(professional)
        code.used = True
        logger.info(f"Profissional criado com ID {db_user.id}")

    elif user.user_type == UserTypeEnum.patient:
        patient = Patient(id=db_user.id)
        db.add(patient)
        logger.info(f"Paciente criado com ID {db_user.id}")

    db.commit()
    return db_user