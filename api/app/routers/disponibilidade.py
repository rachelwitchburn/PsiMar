from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from api.app import crud, schemas, models
from api.app.database_app import get_db
from api.app.security import get_current_usuario

router = APIRouter(prefix="/disponibilidades", tags=["Disponibilidades"])


@router.post("/", response_model=schemas.DisponibilidadeResponse)
def criar_disponibilidade(
    disponibilidade: schemas.DisponibilidadeCreate,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_usuario)
):
    is_admin = usuario.tipo_usuario == models.TipoUsuarioEnum.psicologo
    if not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas psicólogos podem cadastrar disponibilidades."
        )
    return crud.criar_disponibilidade(db, disponibilidade, user_id=usuario.id)


@router.get("/", response_model=List[schemas.DisponibilidadeResponse])
def listar_minhas_disponibilidades(
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_usuario)
):
    is_admin = usuario.tipo_usuario == models.TipoUsuarioEnum.psicologo
    if not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas psicólogos podem ver suas disponibilidades."
        )
    return crud.listar_disponibilidades_por_psicologo(db, psicologo_id=usuario.id)

@router.get("/psicologo/{psicologo_id}", response_model=List[schemas.DisponibilidadeResponse])
def listar_disponibilidades_por_psicologo(
    psicologo_id: int,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_usuario)
):
    return crud.listar_disponibilidades_por_psicologo(db, psicologo_id=psicologo_id)