# app/routes/assistant_routes.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
from ..database import get_db
from .. import models

router = APIRouter()

class AssistantQuery(BaseModel):
    patient_id: int
    command: str

@router.post("/assistant")
def ask_assistant(query: AssistantQuery, db: Session = Depends(get_db)):
    text = query.command.lower()

    # 1. Приветствие
    if "привет" in text:
        return {"response": "Здравствуйте! Чем могу помочь?"}
    
    if "viper" in text:
        return {"response": "viperr, чем могу помочь?"}

    # 2. Помощь
    if "помощь" in text or "help" in text:
        return {"response": "Доступные команды: привет, помощь, время, дата, приемы, врачи, лекарства."}

    # 3. Время
    if "время" in text:
        now = datetime.now().strftime("%H:%M:%S")
        return {"response": f"Текущее время: {now}"}

    # 4. Дата
    if "дата" in text:
        today = datetime.now().strftime("%d.%m.%Y")
        return {"response": f"Сегодняшняя дата: {today}"}

    # 5. Приемы пациента
    if "прием" in text:
        appointments = (
            db.query(models.Appointment)
            .filter(models.Appointment.patient_id == query.patient_id)
            .order_by(models.Appointment.appointment_day.asc())
            .all()
        )
        if not appointments:
            return {"response": "У вас нет записей на прием."}
        dates = ", ".join(a.appointment_day.strftime("%d.%m.%Y") for a in appointments)
        return {"response": f"Ваши записи на приём: {dates}"}

    # 6. Врачи пациента
    if "врач" in text:
        appointments = (
            db.query(models.Appointment)
            .filter(models.Appointment.patient_id == query.patient_id)
            .all()
        )
        names = {
            f"{a.doctor.last_name} {a.doctor.first_name}" for a in appointments if a.doctor
        }
        if not names:
            return {"response": "У вас нет назначенных врачей."}
        docs = ", ".join(names)
        return {"response": f"Ваши врачи: {docs}"}

    # 7. Лекарства пациента
    if "лекарства" in text:
        meds = (
            db.query(models.Medication)
            .join(models.Appointment, models.Medication.appointment_id == models.Appointment.id)
            .filter(models.Appointment.patient_id == query.patient_id)
            .all()
        )
        if not meds:
            return {"response": "У вас нет назначенных лекарств."}
        meds_list = ", ".join(m.medication_name for m in meds)
        return {"response": f"Вам назначены: {meds_list}"}

    # 8. Неизвестная команда
    return {"response": "Извините, я не понял запрос. Попробуйте 'помощь'."}
