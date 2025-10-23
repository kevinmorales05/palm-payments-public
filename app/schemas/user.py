from pydantic import BaseModel,  EmailStr

class UserRead(BaseModel):
    id: int
    email: str
    full_name: str | None = None

    model_config = {
        "from_attributes": True  # reemplaza orm_mode=True en Pydantic v2
    }

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str

    class Config:
        orm_mode = True
