from sqlalchemy.orm import Session
from api.app.models.models import Task, User, UserTypeEnum
from api.app.schemas.task import TaskCreate, TaskUpdate, TaskStatusEnum
from datetime import datetime, timezone
from fastapi import HTTPException, status


def create_task(db: Session, task_data: TaskCreate, professional_id: int):
    patient = db.query(User).filter(User.id == task_data.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado.")
    if patient.user_type != UserTypeEnum.patient:
        raise HTTPException(status_code=400, detail="O ID fornecido não pertence a um paciente.")
    task = Task(
        title=task_data.title,
        description=task_data.description,
        due_date=task_data.due_date,
        patient_id=task_data.patient_id,
        professional_id=professional_id,
        status=TaskStatusEnum.pending.value,
        created_at=datetime.now(timezone.utc)
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_tasks_by_professional(db: Session, professional_id: int):
    return db.query(Task).filter(Task.professional_id == professional_id).all()

def get_tasks_by_patient(db: Session, patient_id: int):
    return db.query(Task).filter(Task.patient_id == patient_id).all()

def get_task_by_id(db: Session, task_id: int):
    """
    Retorna uma tarefa pelo ID.
    """
    return db.query(Task).filter(Task.id == task_id).first()


def update_task_status(db: Session, task_id: int, update_data: TaskUpdate):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada.")

    if update_data.status not in TaskStatusEnum.__members__:
        raise HTTPException(status_code=400, detail="Status de tarefa inválido.")

    task.status = update_data.status
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: int):
    task = get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada.")
    db.delete(task)
    db.commit()