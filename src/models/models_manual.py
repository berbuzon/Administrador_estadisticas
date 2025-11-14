from dataclasses import dataclass
from typing import Optional

@dataclass
class InstitucionManual:
    id: int
    nombre: str
    descripcion: Optional[str] = None

@dataclass
class SedeManual:
    id: int
    nombre: str
    direccion: Optional[str]
    id_institucion: int

@dataclass
class ActividadManual:
    id: int
    valor: str
    vigente: int = 1
