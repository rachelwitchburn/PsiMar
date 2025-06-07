from pydantic import BaseModel, EmailStr, field_validator, model_validator, ConfigDict
from api.app.models.models import UserTypeEnum



class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    user_type: UserTypeEnum
    access_code: str | None = None

    @model_validator(mode="after")
    def check_access_code_for_professional(self):
        if self.user_type == UserTypeEnum.professional and not self.access_code:
            raise ValueError("Profissionais devem fornecer um código de acesso.")
        return self

    @field_validator("password")
    def validate_password(cls, password):
        if len(password) < 6:
            raise ValueError("A senha deve ter pelo menos 6 caracteres.")
        return password

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "first_name": "João",
                    "last_name": "Silva",
                    "email": "joao@example.com",
                    "password": "senha123",
                    "user_type": "patient"
                }
            ]
        }
    )

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    user_type: UserTypeEnum

    model_config = ConfigDict(from_attributes=True)
