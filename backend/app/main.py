from dbm import error
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from .database import SessionLocal
from models import Village,AnnualRainfall
from .schemas import RainFallData, DistrictName, RunoffInput, RunoffOutput, AquiferOutput, StructureInput, StructureOutput


class RunoffInput(BaseModel):
    roof_area: float 
    location: str    
    open_space: float 

class RunoffOutput(BaseModel):
    runoff: float
    feasibility: str
    structure_type: str
    rainfall: float

class AquiferOutput(BaseModel):
    aquifer_type: str
    groundwater_depth: str

class StructureInput(BaseModel):
    runoff_volume: float 
    open_space: float   


app=FastAPI()


def get_location_from_coords_orm(db: Session, lon: float, lat: float):
    point = f'SRID=4326;POINT({lon} {lat})'
    query_result = db.query(Village.dtname).filter(Village.geom.ST_Contains(point)).first()
    if query_result:
        return query_result[0]
    return None

@app.get("/location")
def get_location(lat: float, lon: float, db: Session = Depends(get_db)):
   
    district_name = get_location_from_coords_orm(db, lon, lat)
    if not district_name:
        raise HTTPException(status_code=404, detail="District not found for the provided coordinates.")
    
    return {"district_name": district_name}

@app.get("/location/{district_name}")
def get_rainfall(district_name: str, db: Session = Depends(get_db)):
    try:
        rainfall=db.query(AnnualRainfall.annualrainfall).filter(AnnualRainfall.dtname=={district_name}).first()
        if not rainfall:
            raise HTTPException(status_code=404, detail=f"Rainfall data not found for district: {district_name}")
        return rainfall[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    

@app.post("/calculate-runoff", response_model=RunoffOutput)
def calculate_runoff(data: RunoffInput, db: Session = Depends(get_db)):
    try:
        district_name = data.location
        if ',' in data.location:
            lat, lon = map(float, data.location.split(','))
            district_name = get_location_from_coords_orm(db, lon, lat)
            if not district_name:
                raise HTTPException(status_code=404, detail="Location not found.")

        
        rainfall = db.query(AnnualRainfall).filter(AnnualRainfall.dtname == district_name).first()
        if not rainfall:
            raise HTTPException(status_code=404, detail=f"Rainfall data not found for district: {district_name}")
        rainfall_value = rainfall.annualrainfall

        runoff_coefficients = {
            "concrete": 0.85,
            "metal": 0.90,
            "tiled": 0.80,
            "green": 0.50,
            "unknown": 0.80 
        }
        runoff_coefficient = runoff_coefficients.get(data.roof_type, 0.80)

        
        runoff = (data.roof_area * rainfall_value * runoff_coefficient) / 1000  


        feasibility = "High" if data.roof_area > 100 else "Moderate" if data.roof_area > 50 else "Low"
        structure_type = "Recharge Pit" if data.open_space > 50 else "Recharge Trench" if data.open_space > 20 else "Recharge Shaft"

        return RunoffOutput(
            runoff=round(runoff, 2),
            feasibility=feasibility,
            structure_type=structure_type,
            rainfall=round(rainfall_value, 2),
            runoff_coefficient=round(runoff_coefficient, 2)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {e}")


@app.post("/aquifer-data", response_model=AquiferOutput)
def get_aquifer_data(data: DistrictName, db: Session = Depends(get_db)):  
    try:
        
        aquifer = db.query(Aquifer).filter(Aquifer.dtname == data.dtname).first()
        if not aquifer:
            raise HTTPException(status_code=404, detail=f"Aquifer data not found for district: {data.dtname}")
        
        return AquiferOutput(
            aquifer_type=aquifer.aquifer_type,
            groundwater_depth=aquifer.groundwater_depth
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


@app.post("/recharge-structure", response_model=StructureOutput)
def get_recharge_structure(data: StructureInput, db: Session = Depends(get_db)):
    try:
        length = min(data.open_space * 0.5, 10.0) 
        width = min(data.open_space * 0.3, 5.0)   
        depth = 2.0 if data.runoff_volume > 50 else 1.5  

        volume = length * width * depth
        if volume < data.runoff_volume:
            scale_factor = (data.runoff_volume / volume) ** (1/3)
            length *= scale_factor
            width *= scale_factor
            depth *= scale_factor

        return StructureOutput(
            length=round(length, 2),
            width=round(width, 2),
            depth=round(depth, 2)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {e}")

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "RTRWH FastAPI Backend with Real Datasets", "time": "12:08 AM IST, September 30, 2025"}    