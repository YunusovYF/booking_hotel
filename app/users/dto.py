from pydantic import BaseModel, EmailStr


class SUserAuthDTO(BaseModel):
    email: EmailStr
    password: str


class SUserDTO(BaseModel):
    id: int
    email: EmailStr
