from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.conexiones import get_db
from src.crud.instituciones import get_instituciones
from src.models.schemas import InstitucionOut

router = APIRouter(prefix="/instituciones", tags=["Instituciones"])

@router.get("/", response_model=list[InstitucionOut])
def listar_instituciones(db: Session = Depends(get_db)):
    return get_instituciones(db)
