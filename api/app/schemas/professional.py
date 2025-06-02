from pydantic import BaseModel, ConfigDict, field_validator

class LoginProfessional(BaseModel):
    access_code: str

    @field_validator("access_code")
    def validade_code(cls, code):
        if not code or len(code.strip()) == 0:
            raise ValueError("O código de acesso não pode estar vazio.")
        return code

class ProfessionalOut(BaseModel):
    id: int
    name: str

model_config = ConfigDict(from_attributes=True)