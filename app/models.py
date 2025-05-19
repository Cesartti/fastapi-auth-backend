from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Integer)

class Formulario(Base):
    __tablename__ = "formularios"
    id = Column(Integer, primary_key=True, index=True)
    codigo_catalogo = Column(String)
    descripcion_indicador = Column(String)
    producto_mga = Column(String)
    estado = Column(String, default="pendiente")
    creador_id = Column(Integer)
