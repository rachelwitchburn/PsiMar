from enum import Enum

from pydantic import BaseModel, EmailStr


class UserTypeEnum(str, Enum):
    patient = "patient"
    professional = "professional"


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    user_type: UserTypeEnum


# Para retorno
class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    user_type: UserTypeEnum
    class Config:
        from_attributes = True
