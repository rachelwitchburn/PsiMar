from pydantic import BaseModel, field_validator

class LoginProfessional(BaseModel):
    access_code: str

    @field_validator("access_code")
    def validate_code(cls, code):
        if not code or len(code.strip()) == 0:
            raise ValueError("O código de acesso não pode estar vazio.")
        return code