from sqlalchemy import Column, Integer, String
from src.database.conexiones import Base

class Institucion(Base):
    __tablename__ = "instituciones"
    id = Column(Integer, primary_key=True, index=True)
    valor = Column(String(200))

class Sede(Base):
    __tablename__ = "sedes"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(200))
    direccion = Column(String(255))
    id_institucion = Column(Integer)

class Actividad(Base):
    __tablename__ = "actividades"
    id = Column(Integer, primary_key=True)
    valor = Column(String(255))
    vigente = Column(Integer)
