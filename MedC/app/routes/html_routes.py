# app/routes/html_routes.py
from fastapi import APIRouter, Request, Depends, Form, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from app.utils.generate_pdf import generate_patient_history_pdf,generate_medication_pdf
from fastapi import Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date, timedelta
import os, shutil
from ..data.services import services_by_specialization as viper1
from ..data.medications import medications_list as viper2
from ..auth import get_current_user  # или откуда у вас импортируется

from .. import models
from ..database import SessionLocal

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Главная страница
@router.get("/", response_class=HTMLResponse)
def read_index(request: Request, db: Session = Depends(get_db)):
    today = date.today()
    next_week = today + timedelta(days=7)
    upcoming = (
        db.query(models.Appointment)
          .filter(models.Appointment.appointment_day >= today,
                  models.Appointment.appointment_day <= next_week)
          .order_by(models.Appointment.appointment_day.asc())
          .all()
    )
    return templates.TemplateResponse("index.html", {
        "request": request,
        "upcoming_appointments": upcoming
    })

# Форма записи на приём
@router.get("/appointment", response_class=HTMLResponse)
def appointment_form(request: Request, db: Session = Depends(get_db)):
    patients = db.query(models.Patient).all()
    doctors  = db.query(models.Doctor).all()
    
    return templates.TemplateResponse("appointment.html", {
        "request": request,
        "patients": patients,
        "doctors": doctors,
               "services_by_specialization": viper1
    })

@router.post("/register/appointment")
def register_appointment(
    patient_id: int = Form(...),
    doctor_id:  int = Form(...),
    service:    str = Form(...),
    appointment_day: date = Form(...),
    appointment_time: str = Form(...),
    db: Session = Depends(get_db)
):
    appt = models.Appointment(
        patient_id=patient_id,
        doctor_id=doctor_id,
        service=service,
        appointment_day=appointment_day,
        appointment_time=appointment_time,
        status="Ожидание"
    )
    db.add(appt)
    db.commit()
    return RedirectResponse("/", status_code=302)

# Регистрация пациента
@router.get("/register/patient", response_class=HTMLResponse)
def register_patient_form(request: Request):
    return templates.TemplateResponse("register_patient.html", {"request": request})

@router.post("/register/patient")
def register_patient(
    last_name: str = Form(...),
    first_name: str = Form(...),
    patronymic: str = Form(...),
    gender: str = Form(...),
    date_of_birth: date = Form(...),
    address: str = Form(...),
    phone: str = Form(...),
    insurance_policy: str = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    patient = models.Patient(
        last_name=last_name, first_name=first_name, patronymic=patronymic,
        gender=gender, date_of_birth=date_of_birth, address=address,
        phone=phone, insurance_policy=insurance_policy, email=email
    )
    db.add(patient)
    db.commit()
    return RedirectResponse("/register/patient", status_code=302)

# Регистрация врача
@router.get("/register/doctor", response_class=HTMLResponse)
def register_doctor_form(request: Request, db: Session = Depends(get_db)):
    specializations = [s[0] for s in db.query(models.Doctor.specialization).distinct()]
    cabinets        = [c[0] for c in db.query(models.Doctor.cabinet).distinct()]
    workplaces      = [w[0] for w in db.query(models.Doctor.workplace).distinct()]
    return templates.TemplateResponse("register_doctor.html", {
        "request": request,
        "specializations": specializations,
        "cabinets": cabinets,
        "workplaces": workplaces
    })

@router.post("/register/doctor")
def register_doctor(
    last_name: str = Form(...),
    first_name: str = Form(...),
    patronymic: str = Form(...),
    specialization: str = Form(...),
    cabinet: str = Form(...),
    date_of_birth: date = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    workplace: str = Form(...),
    db: Session = Depends(get_db)
):
    doc = models.Doctor(
        last_name=last_name, first_name=first_name, patronymic=patronymic,
        specialization=specialization, cabinet=cabinet, date_of_birth=date_of_birth,
        phone=phone, email=email, workplace=workplace
    )
    db.add(doc)
    db.commit()
    return RedirectResponse("/register/doctor", status_code=302)

# Поиск записей
@router.get("/search/appointments", response_class=HTMLResponse)
def search_appointments_form(request: Request):
    return templates.TemplateResponse("search_appointments.html", {"request": request})

@router.post("/search/appointments", response_class=HTMLResponse)
def search_appointments(
    request: Request,
    full_name: str = Form(...),
    db: Session = Depends(get_db)
):
    pattern = f"%{full_name.strip()}%"
    # SQLite не поддерживает concat, используем ||
    fullname_field = (
        models.Patient.last_name + " " +
        models.Patient.first_name + " " +
        models.Patient.patronymic
    )
    appts = (
        db.query(models.Appointment)
          .join(models.Patient)
          .filter(fullname_field.ilike(pattern))
          .all()
    )
    return templates.TemplateResponse("search_appointments.html", {
        "request": request,
        "appointments": appts
    })

# Архив записей
@router.get("/archive", response_class=HTMLResponse)
def archive(
    request: Request,
    selected_patient_id: int = 0,
    sort: str = "desc",
    db: Session = Depends(get_db)
):
    today = date.today()
    q = db.query(models.Appointment).filter(models.Appointment.appointment_day < today)
    if selected_patient_id:
        q = q.filter(models.Appointment.patient_id == selected_patient_id)
    q = q.order_by(
        models.Appointment.appointment_day.asc() if sort == "asc" else models.Appointment.appointment_day.desc()
    )
    appts    = q.all()
    patients = db.query(models.Patient).all()
    return templates.TemplateResponse("archive.html", {
        "request": request,
        "appointments": appts,
        "patients": patients,
        "selected_patient_id": selected_patient_id,
        "sort": sort
    })

@router.get("/manage_appointments", response_class=HTMLResponse)
def manage_appointments(
    request: Request,
    patient_id: int = Query(0),
    db: Session = Depends(get_db)
):
    q = db.query(models.Appointment)
    if patient_id:
        q = q.filter(models.Appointment.patient_id == patient_id)
    appts    = q.order_by(models.Appointment.appointment_day.desc()).all()
    patients = db.query(models.Patient).all()
    return templates.TemplateResponse("manage_appointments.html", {
        "request": request,
        "appointments": appts,
        "patients": patients,
        "selected_patient_id": patient_id
    })

# Страница лекарств
@router.get("/medications", response_class=HTMLResponse)
def medications_page(request: Request, db: Session = Depends(get_db)):
    patients  = db.query(models.Patient).all()
    meds_list = [m[0] for m in db.query(models.PharmacyDrug.name).distinct()]
    return templates.TemplateResponse("medications.html", {
        "request": request,
        "patients": patients,
        "medications_list": meds_list
    })

# Назначенные лекарства по записи
@router.get("/medications/{appointment_id}", response_class=HTMLResponse)
def medications_detail(request: Request, appointment_id: int, db: Session = Depends(get_db)):
    appt = db.query(models.Appointment).get(appointment_id)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    meds = db.query(models.Medication).filter(models.Medication.appointment_id == appointment_id).all()
    return templates.TemplateResponse("medication_details.html", {
        "request": request,
        "appointment": appt,
        "medications": meds
    })

# Документы пациента
@router.get("/patients/{patient_id}/documents", response_class=HTMLResponse)
def patient_documents(request: Request, patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).get(patient_id)
    docs    = db.query(models.PatientDocument).filter(models.PatientDocument.patient_id == patient_id).order_by(models.PatientDocument.upload_date.desc()).all()
    return templates.TemplateResponse("patient_documents.html", {
        "request": request,
        "patient": patient,
        "documents": docs
    })

@router.post("/patients/{patient_id}/documents", response_class=RedirectResponse)
def upload_document(
    patient_id: int,
    file: UploadFile = File(...),
    category: str = Form(...),
    db: Session = Depends(get_db)
):
    upload_dir = f"app/static/uploads/{patient_id}/{category}"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    doc = models.PatientDocument(
        patient_id=patient_id,
        category=category,
        filename=file.filename,
        original_name=file.filename,
        upload_date=datetime.utcnow()
    )
    db.add(doc)
    db.commit()
    return RedirectResponse(f"/patients/{patient_id}/documents", status_code=302)

@router.post("/patients/{patient_id}/documents/{doc_id}/delete", response_class=RedirectResponse)
def delete_document(patient_id: int, doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(models.PatientDocument).get(doc_id)
    if doc:
        db.delete(doc)
        db.commit()
    return RedirectResponse(f"/patients/{patient_id}/documents", status_code=302)

# Аптечка
@router.get("/pharmacy", response_class=HTMLResponse)
def pharmacy(request: Request, search: str = "", db: Session = Depends(get_db)):
    q = db.query(models.PharmacyDrug)
    if search:
        q = q.filter(models.PharmacyDrug.name.ilike(f"%{search}%"))
    drugs = q.order_by(models.PharmacyDrug.name).all()
    return templates.TemplateResponse("pharmacy.html", {
        "request": request,
        "drugs": drugs,
        "medications_list": viper2
    })

@router.post("/add_medication", response_class=RedirectResponse)
def add_medication(
    medication_name: str = Form(...),
    dosage: str = Form(...),
    appointment_id: int = Form(...),
    patient_id: int = Form(...),
    db: Session = Depends(get_db)
):
    # Найти лекарство в аптеке по названию
    drug = db.query(models.PharmacyDrug).filter(models.PharmacyDrug.name == medication_name).first()
    med = models.Medication(
        patient_id=patient_id,
        appointment_id=appointment_id,
        pharmacy_drug_id=drug.id if drug else None,
        dosage=dosage
    )
    db.add(med)
    db.commit()
    return RedirectResponse(f"/medications/{appointment_id}", status_code=302)


@router.post("/pharmacy/add", response_class=RedirectResponse)
def add_drug(
    name: str = Form(...),
    dosage: str = Form(...),
    instruction: str = Form(...),
    quantity: int = Form(...),
    db: Session = Depends(get_db)
):
    drug = models.PharmacyDrug(
        name=name, dosage=dosage,
        instruction=instruction, quantity=quantity
    )
    db.add(drug)
    db.commit()
    return RedirectResponse("/pharmacy", status_code=302)

@router.post("/pharmacy/restock/{drug_id}", response_class=RedirectResponse)
def restock_drug(drug_id: int, quantity: int = Form(...), db: Session = Depends(get_db)):
    drug = db.query(models.PharmacyDrug).get(drug_id)
    if drug:
        drug.quantity += quantity
        db.commit()
    return RedirectResponse("/pharmacy", status_code=302)

@router.post("/pharmacy/delete/{drug_id}", response_class=RedirectResponse)
def delete_drug(drug_id: int, db: Session = Depends(get_db)):
    drug = db.query(models.PharmacyDrug).get(drug_id)
    if drug:
        db.delete(drug)
        db.commit()
    return RedirectResponse("/pharmacy", status_code=302)

@router.get("/generate_pdf/drugs/{appointment_id}")
def generate_drugs_pdf(request: Request, appointment_id: int, db: Session = Depends(get_db)):
    # Получаем приём
    appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Приём не найден")
    # Получаем пациента и врача
    patient = appointment.patient
    doctor = appointment.doctor
    # Получаем назначенные лекарства
    medications = db.query(models.Medication).filter(models.Medication.appointment_id == appointment_id).all()
    try:
        pdf_path = generate_medication_pdf(patient, doctor, appointment, medications)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка генерации PDF: {e}")
    return FileResponse(pdf_path, media_type='application/pdf', filename=os.path.basename(pdf_path))

@router.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=302)
    # Удаляем куку из этого же редирект-респонса
    response.delete_cookie(
        key="access_token",
        path="/"           # тот же path, что и при установке
    )
    return response
@router.get("/chatbot", response_class=HTMLResponse)
def chatbot_page(request: Request):
    return templates.TemplateResponse("chatbot.html", {"request": request})