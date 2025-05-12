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

    try:
        hashed_password = pwd_context.hash(user.password)
        logger.info("Senha criptografada com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao criptografar a senha: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao processar a senha.")

    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=str(user.email),
        password=hashed_password,
        user_type=user.user_type
    )

    try:
        logger.info("Tentando adicionar o usuário no banco de dados.")
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        logger.info(f"Usuário criado com ID {db_user.id} e tipo {user.user_type}")
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao salvar o usuário no banco de dados: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao acessar o banco de dados.")

    if user.user_type == UserTypeEnum.professional:
        logger.info(f"Validando código de acesso para profissional: {user.access_code}")
        try:
            code = db.query(AccessCode).filter_by(code=user.access_code).first()
            if not code:
                logger.error(f"Código de acesso {user.access_code} não encontrado no banco.")
            elif code.used:
                logger.error(f"Código de acesso {user.access_code} já foi utilizado.")

            if not code or code.used:
                raise HTTPException(status_code=400, detail="Código de acesso inválido ou já utilizado.")


            professional = Professional(
                id=db_user.id,
                access_code=user.access_code
            )

            db.add(professional)
            code.email = user.email
            code.used = True
            db.commit()

            logger.info(f"Profissional criado com ID {db_user.id}")
        except Exception as e:
            logger.error(f"Erro ao criar profissional ou validar código de acesso: {str(e)}")
            raise HTTPException(status_code=500, detail="Erro ao criar profissional.")

    elif user.user_type == UserTypeEnum.patient:
        try:
            patient = Patient(id=db_user.id)
            db.add(patient)
            logger.info(f"Paciente criado com ID {db_user.id}")
        except Exception as e:
            logger.error(f"Erro ao criar paciente: {str(e)}")
            raise HTTPException(status_code=500, detail="Erro ao criar paciente.")

    try:
        logger.info(f"Tentando confirmar a transação de banco para o usuário {db_user.id}.")
        db.commit()
        logger.info(f"Usuário {db_user.id} registrado com sucesso.")
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao salvar o usuário após criação: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao salvar o usuário.")
    logger.info(f"Usuário {db_user.id} criado com sucesso!")
    return db_user