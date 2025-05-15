from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.database import SessionLocal
from app import models, schemas, auth

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    from jose import JWTError, jwt
    credentials_exception = HTTPException(status_code=401, detail="Invalid credentials")
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_pw = auth.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_pw, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"msg": "Usuario creado"}

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Credenciales inválidas")
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer", "role": user.role, "user_id": user.id}

@router.post("/formulario/")
def crear_formulario(form: schemas.FormularioCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    nuevo = models.Formulario(creado_por=current_user.id, estado="borrador", **form.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/formulario/")
def listar_formularios(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    query = db.query(models.Formulario)
    if current_user.role == 1:
        return query.filter(models.Formulario.creado_por == current_user.id).all()
    elif current_user.role == 2:
        return query.all()
    elif current_user.role == 3:
        return query.filter(models.Formulario.estado == "aprobado").all()

@router.put("/formulario/{formulario_id}")
def actualizar_estado(formulario_id: int, update: schemas.FormularioUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    form = db.query(models.Formulario).filter(models.Formulario.id == formulario_id).first()
    if current_user.role == 2:
        form.estado = update.estado
        form.comentarios = update.comentarios
    elif current_user.role == 1 and form.estado == "devuelto":
        for k, v in update.dict().items():
            if k in form.__dict__ and k not in ["estado", "comentarios"]:
                setattr(form, k, v)
        form.estado = "en revisión"
    elif current_user.role == 3 and form.estado == "aprobado":
        form.estado = "firmado"
        form.firmado_por = current_user.id
    else:
        raise HTTPException(status_code=403, detail="No autorizado para actualizar este formulario")
    db.commit()
    return {"msg": "Formulario actualizado"}
