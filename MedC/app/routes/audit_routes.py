# app/routes/audit_routes.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth import require_roles
from app.database import get_db
from app.models import AuditLog

router = APIRouter()

@router.get("/audit")
def get_audit_log(db: Session = Depends(get_db), current_user = Depends(require_roles("admin"))):
    return db.query(AuditLog).order_by(AuditLog.timestamp.desc()).all()
