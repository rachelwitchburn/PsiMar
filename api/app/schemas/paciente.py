from pydantic import BaseModel, EmailStr, field_validator
from enum import Enum
from typing import Optional

# Usado quando o paciente faz o cadastro completo (senha)
class UsuarioCadastroCompletoPaciente(BaseModel):
    email: EmailStr
    senha: str

    @field_validator("senha")
    def validar_senha(cls, senha):
        if len(senha) < 6:
            raise ValueError("A senha deve ter pelo menos 6 caracteres.")
        return senha
