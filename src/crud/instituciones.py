from sqlalchemy.orm import Session
from src.models.models_orm import Institucion

def get_instituciones(db: Session):
    return db.query(Institucion).all()
