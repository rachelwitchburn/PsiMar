from sqlalchemy.orm import Session
from app.models.models import Professional, AccessCode
from app.schemas.user import UserCreate, UserTypeEnum
from user_crud import create_user
from fastapi import HTTPException

def criar_psicologo(db: Session, dados: UserCreate):
    # Valida código de acesso
    code = db.query(AccessCode).filter_by(codigo=dados.access_code).first()
    if not code or code.utilizado:
        raise HTTPException(status_code=400, detail="Código de acesso inválido ou já utilizado")

    user = create_user(db, dados)

    professional = Professional(
        id=user.id,
        accessCode=dados.access_code
    )
    db.add(professional)

    # Marca código como utilizado
    code.utilizado = True
    db.commit()

    return user

