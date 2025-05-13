from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    last_name = Column(String, index=True)
    first_name = Column(String, index=True)
    patronymic = Column(String, index=True)
    age = Column(Integer)
    gender = Column(String, index=True)
    date_of_birth = Column(String, index=True)
    address = Column(String, index=True)
    phone = Column(String, index=True)
    insurance_policy = Column(String, index=True)
    email = Column(String, index=True)

class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True, index=True)
    last_name = Column(String, index=True)
    first_name = Column(String, index=True)
    patronymic = Column(String, index=True)
    cabinet = Column(String, index=True)
    specialization = Column(String, index=True)
    date_of_birth = Column(String, index=True)
    age = Column(Integer)
    phone = Column(String, index=True)
    email = Column(String, index=True)
    workplace = Column(String, index=True)

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    service = Column(String, index=True)
    appointment_day = Column(Date)
    appointment_time = Column(String)
    status = Column(String, default="Ожидание")
    diagnosis = Column(String)
    recommendations = Column(String)

    patient = relationship("Patient")
    doctor = relationship("Doctor")
    history = relationship("AppointmentHistory", back_populates="appointment")

class AppointmentHistory(Base):
    __tablename__ = "appointment_history"
    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"))
    old_status = Column(String, index=True)
    new_status = Column(String, index=True)
    reason = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    appointment = relationship("Appointment", back_populates="history")

class Medication(Base):
    __tablename__ = "medications"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    appointment_id = Column(Integer, ForeignKey("appointments.id"))
    pharmacy_drug_id = Column(Integer, ForeignKey("pharmacy.id"), nullable=True)
    dosage = Column(String)

    patient = relationship("Patient")
    appointment = relationship("Appointment")
    pharmacy_drug = relationship("PharmacyDrug")

class PatientDocument(Base):
    __tablename__ = "patient_documents"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    category = Column(String, default="Прочее")
    filename = Column(String, index=True)
    original_name = Column(String)
    upload_date = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient")

class PharmacyDrug(Base):
    __tablename__ = "pharmacy"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    dosage = Column(String)
    instruction = Column(String)
    quantity = Column(Integer)
    expiration_date = Column(Date)

    def __repr__(self):
        return f"{self.name} ({self.dosage})"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)

# ✅ Новые модели для тестирования
class Test(Base):
    __tablename__ = "tests"
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    test_id = Column(Integer, ForeignKey("tests.id"))
    text = Column(String)

class Answer(Base):
    __tablename__ = "answers"
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    text = Column(String)
    is_correct = Column(Boolean)

class UserResult(Base):
    __tablename__ = "user_results"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    test_id = Column(Integer, ForeignKey("tests.id"))
    score = Column(Integer)
    submitted_at = Column(DateTime, default=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_log"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    action = Column(String)
    endpoint = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
