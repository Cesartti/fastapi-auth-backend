from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    role: int

class Token(BaseModel):
    access_token: str
    token_type: str
    role: int
    user_id: int

class FormularioCreate(BaseModel):
    codigo_catalogo: str
    descripcion_indicador: str
    producto_mga: str

class FormularioOut(BaseModel):
    id: int
    codigo_catalogo: str
    descripcion_indicador: str
    producto_mga: str
    estado: str
    creador_id: int

    class Config:
        orm_mode = True
