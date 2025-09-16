from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    id: int
    email: EmailStr
    password: str
    mobilenumber: int

class UserCreate(UserBase):
    createdat: datetime
    pass

class DistrictName(BaseModel):
    villname: str
    dtname: str

class RainFallData(BaseModel):
    dtname: str
    annualrainfall: float
