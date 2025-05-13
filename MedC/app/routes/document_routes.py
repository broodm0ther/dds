# routes/document_routes.py

from fastapi import APIRouter, Depends, UploadFile, File, Form, Request
from sqlalchemy.orm import Session
from datetime import datetime
import os
from app.auth import require_roles
from app.database import get_db
from app.models import PatientDocument
from app.utils.audit_logger import log_action

router = APIRouter()


@router.post("/upload")
def upload_document(
    request: Request,
    file: UploadFile = File(...),
    patient_id: int = Form(...),
    category: str = Form("Прочее"),
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "doctor"))
):
    log_action(db, current_user.username, "upload_document", request.url.path)
    upload_dir = f"uploads/patient_{patient_id}"
    os.makedirs(upload_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    filepath = os.path.join(upload_dir, filename)

    with open(filepath, "wb") as f:
        f.write(file.file.read())

    new_doc = PatientDocument(
        patient_id=patient_id,
        category=category,
        filename=filepath,
        original_name=file.filename
    )

    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return {"message": "Файл загружен", "id": new_doc.id}


@router.get("/patient/{id}/documents")
def get_patient_documents(id: int, request: Request, db: Session = Depends(get_db), current_user=Depends(require_roles("admin", "doctor"))):
    log_action(db, current_user.username, "get_patient_documents", request.url.path)
    return db.query(PatientDocument).filter(PatientDocument.patient_id == id).all()
