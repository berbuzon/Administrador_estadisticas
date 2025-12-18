from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.conexiones import get_db
from src.models.models_orm import VistaActividad

router = APIRouter(
    prefix="/reportes",
    tags=["Reportes"]
)

@router.get("/actividad-detalle/")
def actividad_detalle(db: Session = Depends(get_db)):
    """
    Devuelve adolescentes confirmados con actividad e institución
    (sin agregación)
    """
    resultados = (
        db.query(
            VistaActividad.Actividad.label("actividad"),
            VistaActividad.Institucion.label("institucion")
        )
        .all()
    )

    # Convertimos a dicts simples
    return [
        {
            "actividad": r.actividad,
            "institucion": r.institucion
        }
        for r in resultados
    ]
