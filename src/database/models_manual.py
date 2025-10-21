from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

BaseManual = declarative_base()

class RazonSocial(BaseManual):
    """Mapeo MANUAL de [dbo].[RazonSocial]"""
    __tablename__ = 'RazonSocial'
    __table_args__ = {'schema': 'dbo'}

    id = Column(Integer, primary_key=True)
    id_institucion = Column(Integer)
    RazonSocial = Column(String(255))

    def __repr__(self):
        return f"<RazonSocial(id={self.id}, nombre={self.RazonSocial})>"

class Institucion(BaseManual):
    """Mapeo MANUAL de 'instituciones'"""
    __tablename__ = 'instituciones'

    id = Column(Integer, primary_key=True)
    valor = Column(String(100))

    def __repr__(self):
        return f"<Institucion(id={self.id}, valor={self.valor})>"