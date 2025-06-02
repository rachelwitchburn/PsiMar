from pydantic import BaseModel, ConfigDict, EmailStr, field_validator

class PatientCompleteRegistration(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    def validate_password(cls, password):
        if len(password) < 6:
            raise ValueError("A senha deve ter pelo menos 6 caracteres.")
        return password

class PatientOut(BaseModel):
    id: int
    name: str


model_config = ConfigDict(from_attributes=True)