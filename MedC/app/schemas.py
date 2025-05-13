from pydantic import BaseModel, EmailStr, validator
from datetime import datetime, date
from typing import Optional
import re

phone_regex = re.compile(r'^\+?\d{7,15}$')

class PatientCreate(BaseModel):
    last_name: str
    first_name: str
    patronymic: str
    gender: str
    date_of_birth: str
    address: str
    phone: str
    insurance_policy: str
    email: EmailStr
    age: Optional[int] = None

    @validator("phone")
    def validate_phone(cls, value):
        if not phone_regex.match(value):
            raise ValueError("Номер телефона не соответствует формату.")
        return value

    @validator("date_of_birth")
    def validate_date_of_birth(cls, value):
        try:
            dob = datetime.strptime(value, "%Y-%m-%d") if '-' in value else datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Дата рождения должна быть в формате ДД.ММ.ГГГГ или YYYY-MM-DD")
        return dob.strftime("%d.%m.%Y")

    @validator("age", always=True)
    def compute_age(cls, v, values):
        dob_str = values.get("date_of_birth")
        if dob_str:
            dob = datetime.strptime(dob_str, "%d.%m.%Y")
            today = datetime.now()
            return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        raise ValueError("Не удалось вычислить возраст")

class DoctorCreate(BaseModel):
    last_name: str
    first_name: str
    patronymic: str
    cabinet: str
    specialization: str
    date_of_birth: str
    phone: str
    email: EmailStr
    workplace: str
    age: Optional[int] = None

    @validator("phone")
    def validate_phone(cls, value):
        if not phone_regex.match(value):
            raise ValueError("Номер телефона не соответствует формату.")
        return value

    @validator("date_of_birth")
    def validate_date_of_birth(cls, value):
        try:
            dob = datetime.strptime(value, "%Y-%m-%d") if '-' in value else datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Дата рождения должна быть в формате ДД.ММ.ГГГГ или YYYY-MM-DD")
        return dob.strftime("%d.%m.%Y")

    @validator("age", always=True)
    def compute_age(cls, v, values):
        dob_str = values.get("date_of_birth")
        if dob_str:
            dob = datetime.strptime(dob_str, "%d.%m.%Y")
            today = datetime.now()
            return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        raise ValueError("Не удалось вычислить возраст")

class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    service: str
    appointment_day: date
    appointment_time: str

# ✅ Схема для регистрации пользователя
class UserCreate(BaseModel):
    username: str
    password: str
    role: str
from pydantic import BaseModel
from typing import List

class AnswerCreate(BaseModel):
    text: str
    is_correct: bool

class QuestionCreate(BaseModel):
    text: str
    answers: List[AnswerCreate]

class TestCreate(BaseModel):
    name: str
    questions: List[QuestionCreate]

class AnswerSubmission(BaseModel):
    question_id: int
    selected_answer_ids: List[int]

class TestSubmission(BaseModel):
    answers: List[AnswerSubmission]
