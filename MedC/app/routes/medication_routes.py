# routes/medication_routes.py

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.auth import require_roles
from app.database import get_db
from app.models import Medication
from app.utils.audit_logger import log_action

router = APIRouter()


@router.post("/prescribe")
def prescribe_medication(request: Request, data: dict, db: Session = Depends(get_db), current_user=Depends(require_roles("doctor"))):
    log_action(db, current_user.username, "prescribe_medication", request.url.path)
    new = Medication(**data)
    db.add(new)
    db.commit()
    db.refresh(new)
    return new


@router.get("/medications")
def get_all_medications(request: Request, db: Session = Depends(get_db), current_user=Depends(require_roles("admin", "doctor"))):
    log_action(db, current_user.username, "get_all_medications", request.url.path)
    return db.query(Medication).all()
