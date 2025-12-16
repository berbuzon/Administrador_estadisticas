from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database.conexiones import get_db
from src.crud.actividades import get_actividades
from src.models.schemas import ActividadOut

router = APIRouter(prefix="/actividades", tags=["Actividades"])

@router.get("/", response_model=list[ActividadOut])
def listar_actividades(db: Session = Depends(get_db)):
    return get_actividades(db)
