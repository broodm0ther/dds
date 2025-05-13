# app/utils/audit_logger.py

from app.models import AuditLog
from datetime import datetime

def log_action(db, username: str, action: str, endpoint: str):
    entry = AuditLog(
        username=username,
        action=action,
        endpoint=endpoint,
        timestamp=datetime.utcnow()
    )
    db.add(entry)
    db.commit()
