from pydantic import BaseModel
from typing import Optional


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
    valor: str
    direccion: Optional[str] = None
    institucion_id: int
    class Config:
        from_attributes = True
