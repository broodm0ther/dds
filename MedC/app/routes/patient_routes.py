# routes/patient_routes.py

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.auth import require_roles
from app.database import get_db
from app.models import Patient
from app.utils.generate_pdf import generate_patient_history_pdf
from app.utils.audit_logger import log_action

router = APIRouter()


@router.post("/register/patient")
def register_patient(request: Request, patient: dict, db: Session = Depends(get_db), current_user=Depends(require_roles("admin", "registrar"))):
    log_action(db, current_user.username, "register_patient", request.url.path)
    new = Patient(**patient)
    db.add(new)
    db.commit()
    db.refresh(new)
    return new


@router.get("/patients/{patient_id}/export-history")
def export_history(patient_id: int, request: Request, db: Session = Depends(get_db), current_user=Depends(require_roles("admin", "doctor"))):
    log_action(db, current_user.username, "export_patient_history", request.url.path)
    pdf_path = generate_patient_history_pdf(patient_id, db)
    return {"pdf": pdf_path}


@router.get("/api/patients")
def get_all_patients(request: Request, db: Session = Depends(get_db), current_user=Depends(require_roles("admin", "doctor", "registrar"))):
    log_action(db, current_user.username, "get_all_patients", request.url.path)
    return db.query(Patient).all()
