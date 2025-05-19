from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from . import models, schemas, auth
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "secret"
ALGORITHM = "HS256"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(username=user.username, hashed_password=hashed_password, role=user.role)
    db.add(new_user)
    db.commit()
    return {"msg": "Usuario creado"}

@app.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Credenciales inválidas")
    access_token = auth.create_access_token(data={"sub": user.username, "role": user.role, "user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer", "role": user.role, "user_id": user.id}

@app.post("/formulario")
def crear_formulario(form: schemas.FormularioCreate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    nuevo = models.Formulario(**form.dict(), creador_id=user.id)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@app.get("/formulario", response_model=list[schemas.FormularioOut])
def listar_formularios(user=Depends(get_current_user), db: Session = Depends(get_db)):
    if user.role == 1:
        return db.query(models.Formulario).filter_by(creador_id=user.id).all()
    elif user.role == 2:
        return db.query(models.Formulario).filter(models.Formulario.estado != "firmado").all()
    elif user.role == 3:
        return db.query(models.Formulario).filter_by(estado="aprobado").all()
    else:
        raise HTTPException(status_code=403, detail="Rol no autorizado")
