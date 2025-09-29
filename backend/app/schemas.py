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

class RunoffInput(BaseModel):
    roof_area: float
    location: str
    open_space: float
    roof_type: Literal["concrete", "metal", "tiled", "green", "unknown"]  

class RunoffOutput(BaseModel):
    runoff: float
    feasibility: str
    structure_type: str
    rainfall: float
    runoff_coefficient: float  

class AquiferOutput(BaseModel):
    aquifer_type: str
    groundwater_depth: str

class StructureInput(BaseModel):
    runoff_volume: float
    open_space: float

class StructureOutput(BaseModel):
    length: float
    width: float
    depth: float    
