# routes/doctor_routes.py

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.auth import require_roles
from app.database import get_db
from app.models import Doctor
from app.utils.audit_logger import log_action

router = APIRouter()


@router.post("/register/doctor")
def register_doctor(request: Request, doctor: dict, db: Session = Depends(get_db), current_user=Depends(require_roles("admin"))):
    log_action(db, current_user.username, "register_doctor", request.url.path)
    new = Doctor(**doctor)
    db.add(new)
    db.commit()
    db.refresh(new)
    return new


@router.get("/api/doctors")
def get_all_doctors(request: Request, db: Session = Depends(get_db), current_user=Depends(require_roles("admin", "doctor", "registrar"))):
    log_action(db, current_user.username, "get_all_doctors", request.url.path)
    return db.query(Doctor).all()
