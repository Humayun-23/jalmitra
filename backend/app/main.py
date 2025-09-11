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