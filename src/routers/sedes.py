from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.conexiones import get_db
from src.crud.sedes import get_sedes
from src.models.schemas import SedeOut

router = APIRouter(prefix="/sedes", tags=["Sedes"])

@router.get("/", response_model=list[SedeOut])
def listar_sedes(db: Session = Depends(get_db)):
    return get_sedes(db)
