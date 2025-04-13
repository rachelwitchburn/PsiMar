from pydantic import BaseModel, EmailStr, field_validator


class LoginCredential(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    def validate_password(self, password):
        if len(password) < 6:
            raise ValueError("A senha deve ter pelo menos 6 caracteres.")
        return password