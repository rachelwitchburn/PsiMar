from pydantic import BaseModel, EmailStr

class LoginProfessional(BaseModel):
    access_code: str