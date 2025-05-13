# app/utils/export_excel.py

import os
import pandas as pd
from datetime import datetime

def export_pharmacy_to_excel(db):
    from app.models import PharmacyDrug

    drugs = db.query(PharmacyDrug).all()
    data = [{
        "ID": drug.id,
        "Название": drug.name,
        "Дозировка": drug.dosage,
        "Инструкция": drug.instruction,
        "Остаток": drug.quantity,
        "Срок годности": drug.expiration_date.strftime("%d.%m.%Y") if drug.expiration_date else ""
    } for drug in drugs]

    df = pd.DataFrame(data)
    os.makedirs("exports", exist_ok=True)
    filename = f"exports/pharmacy_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    df.to_excel(filename, index=False)
    return filename
