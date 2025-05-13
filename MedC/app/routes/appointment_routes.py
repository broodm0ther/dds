# routes/appointment_routes.py

from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.auth import require_roles
from app.database import get_db
from app.models import Appointment, AppointmentHistory
from app.utils.audit_logger import log_action

router = APIRouter()


@router.get("/appointments")
def list_appointments(request: Request, db: Session = Depends(get_db), current_user=Depends(require_roles("admin", "doctor", "registrar"))):
    log_action(db, current_user.username, "list_appointments", request.url.path)
    return db.query(Appointment).all()


@router.post("/register/appointment")
def create_appointment(request: Request, appointment: dict, db: Session = Depends(get_db), current_user=Depends(require_roles("admin", "registrar"))):
    log_action(db, current_user.username, "create_appointment", request.url.path)
    new = Appointment(**appointment)
    db.add(new)
    db.commit()
    db.refresh(new)
    return new


@router.patch("/appointments/{id}/status")
def update_appointment_status(id: int, payload: dict, request: Request, db: Session = Depends(get_db), current_user=Depends(require_roles("admin", "doctor"))):
    log_action(db, current_user.username, "update_appointment_status", request.url.path)
    appointment = db.query(Appointment).filter(Appointment.id == id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Приём не найден")

    history = AppointmentHistory(
        appointment_id=id,
        old_status=appointment.status,
        new_status=payload["new_status"],
        reason=payload.get("reason")
    )

    appointment.status = payload["new_status"]
    db.add(history)
    db.commit()
    return {"message": "Статус обновлён"}


@router.patch("/appointments/{id}/diagnosis")
def add_diagnosis_and_recommendations(id: int, payload: dict, request: Request, db: Session = Depends(get_db), current_user=Depends(require_roles("doctor"))):
    log_action(db, current_user.username, "add_diagnosis", request.url.path)
    appointment = db.query(Appointment).filter(Appointment.id == id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Приём не найден")

    appointment.diagnosis = payload.get("diagnosis", "")
    appointment.recommendations = payload.get("recommendations", "")
    db.commit()
    return {"message": "Диагноз и рекомендации обновлены"}
