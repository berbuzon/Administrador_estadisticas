from sqlalchemy.orm import Session
from sqlalchemy import func

from src.models.models_orm import VistaActividad, VistaEdadSexo


# ---------------------------------------------------
# REPORTES GENERALES
# ---------------------------------------------------

def total_adolescentes(db: Session):
    return db.query(func.count(VistaActividad.id_adolescente.distinct())).scalar()


def adolescentes_por_categoria(db: Session):
    return (
        db.query(VistaActividad.Categoria, func.count())
        .group_by(VistaActividad.Categoria)
        .order_by(func.count().desc())
        .all()
    )


def adolescentes_por_institucion(db: Session):
    return (
        db.query(VistaActividad.Institucion, func.count())
        .group_by(VistaActividad.Institucion)
        .order_by(func.count().desc())
        .all()
    )


def adolescentes_por_actividad(db: Session):
    return (
        db.query(VistaActividad.Actividad, func.count())
        .group_by(VistaActividad.Actividad)
        .order_by(func.count().desc())
        .all()
    )


def top10_instituciones(db: Session):
    return (
        db.query(VistaActividad.Institucion, func.count())
        .group_by(VistaActividad.Institucion)
        .order_by(func.count().desc())
        .limit(10)
        .all()
    )


def top10_actividades(db: Session):
    return (
        db.query(VistaActividad.Actividad, func.count())
        .group_by(VistaActividad.Actividad)
        .order_by(func.count().desc())
        .limit(10)
        .all()
    )


# ---------------------------------------------------
# REPORTES DEMOGRÁFICOS
# ---------------------------------------------------

from sqlalchemy import func

def adolescentes_por_tramo_edad(db: Session):
    return (
        db.query(
            VistaEdadSexo.tramo_edad, 
            func.count(VistaEdadSexo.id_adolescente)
        )
        .group_by(VistaEdadSexo.tramo_edad)
        .order_by(func.count(VistaEdadSexo.id_adolescente).desc())
        .all()
    )



def adolescentes_por_genero(db: Session):
    return (
        db.query(VistaEdadSexo.genero, func.count())
        .group_by(VistaEdadSexo.genero)
        .order_by(func.count().desc())
        .all()
    )
