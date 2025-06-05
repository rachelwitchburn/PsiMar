from fastapi import HTTPException, status
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.app.database_app import get_db
from api.app.models.models import User, UserTypeEnum
from api.app.crud import patient_service
from api.app.security import get_current_user
from api.app.schemas.patient import PatientOut
from typing import List

router = APIRouter(prefix="/patient", tags=["patient"])


@router.get("/list", response_model=List[PatientOut])
async def list_patients(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if current_user.user_type != UserTypeEnum.professional:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas profissionais podem listar pacientes."
        )

    patients = patient_service.get_all_patients(db)
    return patients



