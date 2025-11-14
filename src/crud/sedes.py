from sqlalchemy.orm import Session
from src.models.models_orm import Sede

def get_sedes(db: Session):
    return db.query(Sede).all()
