from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    id: int
    email: EmailStr
    password: str
    mNumber: int

class UserCreate(UserBase):
    pass

class DistrictList(BaseModel):
    villName: str
    dtName: str

class RainFallData(BaseModel):
    