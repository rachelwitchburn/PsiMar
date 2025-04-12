from pydantic import BaseModel, EmailStr

class UsuarioPreCadastro(BaseModel):
    email: EmailStr
