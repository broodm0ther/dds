from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
from app.models import PharmacyDrug
from app.auth import require_roles
from app.database import get_db

router = APIRouter()


@router.get("/pharmacy/expired")
def list_expired(db: Session = Depends(get_db), current_user = Depends(require_roles("admin"))):
    return db.query(PharmacyDrug).filter(PharmacyDrug.expiration_date < date.today()).all()

@router.get("/pharmacy/low-stock")
def list_low_stock(db: Session = Depends(get_db), current_user = Depends(require_roles("admin"))):
    return db.query(PharmacyDrug).filter(PharmacyDrug.quantity < 5).all()

@router.post("/pharmacy/add")
def add_drug(drug: dict, db: Session = Depends(get_db), current_user = Depends(require_roles("admin"))):
    new = PharmacyDrug(**drug)
    db.add(new)
    db.commit()
    db.refresh(new)
    return new

@router.delete("/pharmacy/delete_expired")
def delete_expired(db: Session = Depends(get_db), current_user = Depends(require_roles("admin"))):
    expired = db.query(PharmacyDrug).filter(PharmacyDrug.expiration_date < date.today()).all()
    for drug in expired:
        db.delete(drug)
    db.commit()
    return {"deleted": len(expired)}

