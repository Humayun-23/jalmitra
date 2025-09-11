from sqlalchemy import Column, Float, Integer, String
from geoalchemy2 import Geometry
from database import Base


class Village(Base):
    __tablename__ = "villages"

    
    id = Column(Integer, primary_key=True, index=True)
    vilname=Column(String,nullable=False)
    stname=Column(String,nullable=False)
    dtname = Column(String, index=True)
    geom = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326))

class AnnualRainfall(Base):
    dtname=Column(String,nullable=False)
    annualrainfall=Column(Float,nullable=True)