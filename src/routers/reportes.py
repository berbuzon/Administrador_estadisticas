from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.models.models_orm import VistaActividad

from src.database.conexiones import get_db
from src.reports.adolescentes import (
    total_adolescentes,
    adolescentes_por_categoria,
    adolescentes_por_institucion,
    adolescentes_por_actividad,
    top10_instituciones,
    top10_actividades,
    adolescentes_por_tramo_edad,
    adolescentes_por_genero,
)

router = APIRouter(prefix="/reportes", tags=["Reportes"])


@router.get("/total")
def _total(db: Session = Depends(get_db)):
    return {"total_adolescentes": total_adolescentes(db)}


@router.get("/categoria")
def _categoria(db: Session = Depends(get_db)):
    datos = adolescentes_por_categoria(db)
    return [{"categoria": fila[0], "cantidad": fila[1]} for fila in datos]


@router.get("/institucion")
def _institucion(db: Session = Depends(get_db)):
    datos = adolescentes_por_institucion(db)
    return [{"institucion": fila[0], "cantidad": fila[1]} for fila in datos]


@router.get("/actividad")
def _actividad(db: Session = Depends(get_db)):
    datos = adolescentes_por_actividad(db)
    return [{"actividad": fila[0], "cantidad": fila[1]} for fila in datos]


@router.get("/top10-instituciones")
def _top10i(db: Session = Depends(get_db)):
    datos = top10_instituciones(db)
    return [{"institucion": fila[0], "cantidad": fila[1]} for fila in datos]


@router.get("/top10-actividades")
def _top10a(db: Session = Depends(get_db)):
    datos = top10_actividades(db)
    return [{"actividad": fila[0], "cantidad": fila[1]} for fila in datos]


@router.get("/tramo-edad")
def _edad(db: Session = Depends(get_db)):
    datos = adolescentes_por_tramo_edad(db)
    return [{"tramo_edad": fila[0], "cantidad": fila[1]} for fila in datos]


@router.get("/genero")
def _genero(db: Session = Depends(get_db)):
    datos = adolescentes_por_genero(db)
    return [{"genero": fila[0], "cantidad": fila[1]} for fila in datos]

@router.get("/actividad-detalle")
def actividad_detalle(db: Session = Depends(get_db)):
    """
    Devuelve adolescentes confirmados con actividad e institución
    (una fila por adolescente)
    """
    resultados = (
        db.query(
            VistaActividad.Actividad.label("actividad"),
            VistaActividad.Institucion.label("institucion")
        )
        .all()
    )

    return [
        {
            "actividad": r.actividad,
            "institucion": r.institucion
        }
        for r in resultados
    ]
