# routes/appointment_routes.py

from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from datetime import date
from app.auth import require_roles
from app.database import get_db
from app.models import Appointment, AppointmentHistory
from app.utils.audit_logger import log_action
import app.models as models

router = APIRouter()


@router.get("/appointments")
def list_appointments(request: Request, db: Session = Depends(get_db), current_user=Depends(require_roles("admin", "doctor", "registrar"))):
    log_action(db, current_user.username, "list_appointments", request.url.path)
    return db.query(Appointment).all()



# Получить записи пациента (AJAX)
@router.get("/get_appointments/{patient_id}", response_class=JSONResponse)
def get_appointments(patient_id: int, db: Session = Depends(get_db)):
    appts = (
        db.query(models.Appointment)
          .filter(models.Appointment.patient_id == patient_id,
                  models.Appointment.appointment_day >= date.today())
          .order_by(models.Appointment.appointment_day.desc())
          .all()
    )
    data = [
        {
            "id": a.id,
            "doctor": f"{a.doctor.last_name} {a.doctor.first_name}",
            "specialization": a.doctor.specialization,
            "service": a.service,
            "date": a.appointment_day.strftime("%d.%m.%Y"),
            "time": a.appointment_time
        }
        for a in appts
    ]
    return JSONResponse(content=data)

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
