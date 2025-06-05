from pydantic import BaseModel, EmailStr, field_validator, ConfigDict, Field

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginCredential(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, description="Senha não pode ser vazia")

    @field_validator("password")
    def validate_password(cls, password):
        if len(password) < 6:
            raise ValueError("A senha deve ter pelo menos 6 caracteres.")
        return password

class LoginData(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, description="Senha não pode ser vazia")

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{"email": "usuario@example.com", "password": "senha123"}]
        }
    )

class ResetPassword(BaseModel):
    nova_senha: str = Field(min_length=6, description="Senha deve ter pelo menos 6 caracteres")

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{"nova_senha": "novasenha456"}]
        }
    )

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_type: str
    user_id: int

class ResetPasswordWithToken(BaseModel):
    token: str = Field(..., description="Token de redefinição de senha")
    nova_senha: str = Field(min_length=6, description="Senha deve ter pelo menos 6 caracteres")

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "nova_senha": "novasenha456"
            }]
        }
    )

class ForgotPasswordRequest(BaseModel):
    email: EmailStr