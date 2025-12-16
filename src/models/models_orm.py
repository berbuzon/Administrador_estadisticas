from sqlalchemy import Column, Integer, String
from src.database.conexiones import Base

# ---------------------------------------------------------
# TABLAS REALES (Minimales para tus endpoints actuales)
# ---------------------------------------------------------

class Institucion(Base):
    __tablename__ = "instituciones"

    id = Column(Integer, primary_key=True)
    valor = Column(String(200))


class Sede(Base):
    __tablename__ = "sedes"

    id = Column(Integer, primary_key=True)
    valor = Column(String(200))
    direccion = Column(String(255))
    institucion_id = Column(Integer)


class Actividad(Base):
    __tablename__ = "actividades"

    id = Column(Integer, primary_key=True)
    valor = Column(String(255))
    vigente = Column(Integer)


# ---------------------------------------------------------
# VISTAS PARA REPORTES
# ---------------------------------------------------------

class VistaActividad(Base):
    __tablename__ = "vista_adolescentes_confirmados_segun_actividad"

    id_adolescente = Column(Integer, primary_key=True)
    Nombre = Column(String(100))
    Apellido = Column(String(100))
    DNI = Column(String(20))

    Institucion = Column(String(255))
    Sede = Column(String(255))
    Actividad = Column(String(255))
    Dia = Column(String(50))
    Horario = Column(String(100))

    categoria_id = Column(Integer)
    Categoria = Column(String(255))



class VistaEdadSexo(Base):
    __tablename__ = "vista_adolescentes_confirmados_segun_edad_sexo"

    id_adolescente = Column(Integer, primary_key=True)
    Nombre = Column(String(100))
    Apellido = Column(String(100))
    DNI = Column(String(20))
    fecha_nacimiento = Column(String(20))
    edad2025 = Column(Integer)
    genero = Column(String(20))
    tramo_edad = Column(String(50))

