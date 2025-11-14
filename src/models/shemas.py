from pydantic import BaseModel

# -------- ACTIVIDAD --------
class ActividadOut(BaseModel):
    id: int
    valor: str
    vigente: int
    class Config:
        from_attributes = True

# -------- INSTITUCION --------
class InstitucionOut(BaseModel):
    id: int
    valor: str
    class Config:
        from_attributes = True

# -------- SEDE --------
class SedeOut(BaseModel):
    id: int
    nombre: str
    direccion: str
    id_institucion: int
    class Config:
        from_attributes = True
