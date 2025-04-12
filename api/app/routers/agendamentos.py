from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.app import crud, models, schemas
from api.app.database_app import get_db

router = APIRouter()

@router.post("/agendar/", response_model=schemas.AgendamentoResponse)
def agendar_consulta(
    paciente_id: int,
    disponibilidade_id: int,
    db: Session = Depends(get_db)
):
    try:
        agendamento = crud.agendar_consulta(db, paciente_id, disponibilidade_id)
        return agendamento
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))