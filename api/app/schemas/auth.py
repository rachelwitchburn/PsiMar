from pydantic import BaseModel, EmailStr, field_validator, ConfigDict

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginCredential(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    def validate_password(cls, password):
        if len(password) < 6:
            raise ValueError("A senha deve ter pelo menos 6 caracteres.")
        return password

class LoginData(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{"email": "usuario@example.com", "password": "senha123"}]
        }
    )

class ResetPassword(BaseModel):
    nova_senha: str

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{"nova_senha": "novasenha456"}]
        }
    )

class TokenResponse(BaseModel):
    access_token: str
    token_type: str