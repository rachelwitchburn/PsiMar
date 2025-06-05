from pydantic import BaseModel, ConfigDict, model_validator
from datetime import datetime, timezone
from typing import Optional
from enum import Enum
from typing_extensions import Self

class TaskStatusEnum(str, Enum):
    pending = 'pending'
    completed = 'completed'


class TaskBase(BaseModel):
    description: str
    due_date: Optional[datetime]

    @model_validator(mode='after')
    def validate_due_date(self) -> Self:
        print(f"Due date type: {type(self.due_date)}")
        print(f"Due date value: {self.due_date}")
        # Garantir que são cientes de fuso horário
        if self.due_date is not None:
            # Se due_date for naive, converter para aware (timezone UTC)
            if self.due_date.tzinfo is None:
                self.due_date = self.due_date.replace(tzinfo=timezone.utc)

            if self.due_date < datetime.now(timezone.utc):
                raise ValueError("A data de entrega não pode estar no passado.")

        return self

class TaskCreate(TaskBase):
    patient_id: int
    title: str


class TaskUpdate(BaseModel):
    status: TaskStatusEnum


class TaskOut(TaskBase):
    id: int
    title: str
    status: TaskStatusEnum
    created_at: datetime
    patient_id: int
    professional_id: int

    model_config = ConfigDict(from_attributes=True)