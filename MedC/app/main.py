from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import create_access_token, get_current_user
from sqlalchemy.orm import Session
from .routes import (
    patient_router, 
    doctor_router, 
    html_router, 
    appointment_router, 
    medication_router, 
    archive_router,
    document_router,
    assistant_routes  # ✅ Добавлено
)
from . import models, schemas
from .database import engine, get_db
from .routes.training_routes import router as training_router
from .routes.audit_routes import router as audit_router
import bcrypt

app = FastAPI(title="Медицинская организация")

models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(html_router)
app.include_router(patient_router)
app.include_router(doctor_router)
app.include_router(appointment_router)
app.include_router(medication_router)
app.include_router(archive_router)
app.include_router(document_router)
app.include_router(assistant_routes.router)
app.include_router(training_router)
app.include_router(audit_router)

# ✅ Эндпоинт для регистрации пользователей
@app.post("/register_user")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

    new_user = models.User(
        username=user.username,
        hashed_password=hashed_password.decode('utf-8'),
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    if not bcrypt.checkpw(form_data.password.encode('utf-8'), user.hashed_password.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer", "role": user.role}

@app.get("/protected")
def protected_route(current_user: models.User = Depends(get_current_user)):
    return {"username": current_user.username, "role": current_user.role}
