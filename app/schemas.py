from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    role: int

class UserLogin(BaseModel):
    username: str
    password: str

class FormularioBase(BaseModel):
    codigo_catalogo: str
    medido_a_traves: str
    descripcion_indicador: str
    producto_mga: str
    tipo_indicador: str
    linea_base: float
    meta_cuatrienio: float
    vigencia: str
    valor_modificado: float
    total_programado: float
    aporte_proyecto: float
    porcentaje_aporte: float
    valor_final: float
    aporte_acumulado: float
    porcentaje_total_aporte: float

class FormularioCreate(FormularioBase):
    pass

class FormularioUpdate(FormularioBase):
    comentarios: str
    estado: str

class FormularioResponse(FormularioBase):
    id: int
    estado: str
    comentarios: str
    creado_por: int
    firmado_por: int | None

    class Config:
        orm_mode = True
