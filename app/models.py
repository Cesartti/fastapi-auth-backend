from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Integer)  # 1 = creador, 2 = validador, 3 = firmante

class Formulario(Base):
    __tablename__ = "formularios"
    id = Column(Integer, primary_key=True, index=True)
    creado_por = Column(Integer, ForeignKey("users.id"))
    estado = Column(String, default="borrador")
    comentarios = Column(String, default="")
    firmado_por = Column(Integer, ForeignKey("users.id"), nullable=True)

    codigo_catalogo = Column(String)
    medido_a_traves = Column(String)
    descripcion_indicador = Column(String)
    producto_mga = Column(String)
    tipo_indicador = Column(String)
    linea_base = Column(Float)
    meta_cuatrienio = Column(Float)
    vigencia = Column(String)
    valor_modificado = Column(Float)
    total_programado = Column(Float)
    aporte_proyecto = Column(Float)
    porcentaje_aporte = Column(Float)
    valor_final = Column(Float)
    aporte_acumulado = Column(Float)
    porcentaje_total_aporte = Column(Float)
