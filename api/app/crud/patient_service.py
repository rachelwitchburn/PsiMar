from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.models import Patient, User
from app.schemas.user import UserCreate
from user_crud import create_user


def criar_paciente(db: Session, dados: UserCreate):
    user = db.query(User).filter_by(email=dados.email).first() # para user precadastrado
    if not user:
        raise HTTPException(status_code=404, detail="E-mail não pré-cadastrado")
    if user.senha:
        raise HTTPException(status_code=400, detail="Cadastro já realizado")

    user.senha = dados.password  # hash vai ser aplicado no usuário_base se quiser
    user.user_type = dados.user_type
    user.senha = create_user(db, dados).password

    paciente = Patient(id=user.id)
    db.add(paciente)
    db.commit()

    return user
