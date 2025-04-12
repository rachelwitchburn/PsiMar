from pydantic import BaseModel, EmailStr, field_validator
from enum import Enum
from typing import Optional

# Usado quando o paciente faz o cadastro completo (password)
class PatientCompleteRegistration(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    def validate_password(cls, password):
        if len(password) < 6:
            raise ValueError("A password deve ter pelo menos 6 caracteres.")
        return password
