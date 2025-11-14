from sqlalchemy.orm import Session
from src.models.models_orm import Actividad

def get_actividades(db: Session):
    return db.query(Actividad).all()
