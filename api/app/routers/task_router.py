from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.app.schemas.task import TaskCreate, TaskOut, TaskUpdate
from api.app.crud import task_service
from api.app.security import get_db, get_current_user
from api.app.models.models import User, UserTypeEnum
from typing import List
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# Função de verificação de permissão de usuário
async def verify_user_permission(current_user: User, task):
    if task is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada.")
    match current_user.user_type:
        case UserTypeEnum.patient if task.patient_id != current_user.id:
            logger.warning(f"[TASK ROUTER] Acesso negado: paciente {current_user.id} tentou acessar a tarefa {task.id}")
            raise HTTPException(status_code=403, detail="Não autorizado a acessar essa tarefa.")
        case UserTypeEnum.professional if task.professional_id != current_user.id:
            logger.warning(f"[TASK ROUTER] Acesso negado: profissional {current_user.id} tentou acessar a tarefa {task.id}")
            raise HTTPException(status_code=403, detail="Não autorizado a acessar essa tarefa.")
        case _ if current_user.user_type not in [UserTypeEnum.patient, UserTypeEnum.professional]:
            logger.warning(f"[TASK ROUTER] Acesso negado: tipo de usuário inválido ({current_user.user_type}) tentou acessar uma tarefa.")
            raise HTTPException(status_code=403, detail="Tipo de usuário não autorizado.")


@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
     Permite que um profissional crie uma nova tarefa para um paciente.
    """
    if current_user.user_type != UserTypeEnum.professional:
        raise HTTPException(status_code=403, detail="Somente profissionais podem criar tarefas.")
    patient = db.query(User).filter(User.id == task.patient_id).first()
    if not patient or patient.user_type != UserTypeEnum.patient:
        raise HTTPException(status_code=400, detail="Paciente inválido.")
    new_task = task_service.create_task(db, task, current_user.id)
    logger.info(f"[TASK ROUTER] Tarefa criada pelo profissional {current_user.id} para paciente {task.patient_id}")
    return new_task


# Rota para o profissional visualizar todas as tarefas
@router.get("/professional/assigned", response_model=List[TaskOut])
async def get_assigned_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
     Retorna todas as tarefas atribuídas pelo profissional logado.
    """
    if current_user.user_type != UserTypeEnum.professional:
        raise HTTPException(status_code=403, detail="Somente profissionais podem visualizar as tarefas designadas.")
    return task_service.get_tasks_by_professional(db, current_user.id)

@router.get("/patient", response_model=List[TaskOut])
async def get_my_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
     Retorna todas as tarefas atribuídas ao paciente logado.
    """
    if current_user.user_type != UserTypeEnum.patient:
        raise HTTPException(status_code=403, detail="Somente pacientes podem ver suas tarefas.")
    return task_service.get_tasks_by_patient(db, current_user.id)

@router.get("/{task_id}", response_model=TaskOut)
async def get_task_by_id(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
         Retorna uma tarefa específica pelo ID, com base no usuário autenticado.
    """
    task = task_service.get_task_by_id(db, task_id)
    await verify_user_permission(current_user, task)
    return task

@router.patch("/{task_id}", response_model=TaskOut)
async def update_task_status(
    task_id: int,
    update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
      Permite que pacientes atualizem o status de suas tarefas.
      Profissionais também podem modificar tarefas que eles criaram.
    """
    task = task_service.get_task_by_id(db, task_id)
    await verify_user_permission(current_user, task)
    updated = task_service.update_task_status(db, task_id, update)
    logger.info(f"[TASK ROUTER] Tarefa {task_id} atualizada por usuário {current_user.id}")
    return updated

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
     Permite que profissionais excluam tarefas que criaram.
    """
    task = task_service.get_task_by_id(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada.")
    await verify_user_permission(current_user, task)
    if current_user.user_type != UserTypeEnum.professional or current_user.id != task.professional_id:
        raise HTTPException(status_code=403, detail="Somente profissionais podem excluir tarefas.")
    task_service.delete_task(db, task_id)
    logger.info(f"[TASK ROUTER] Tarefa {task_id} deletada pelo profissional {current_user.id}")