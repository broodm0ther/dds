# app/routes/assistant_routes.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import google.generativeai as genai

router = APIRouter()

# ✅ Список API-ключей Gemini (ротация при ошибках)
API_KEYS = [
    "AIzaSyBjd0PciFa82NJHW4cRklWcwthLm7Puym4",
    "AIzaSyAu-NpbHQfJZT4h4W9Qdn9BjrFFkm4SPeU",
    "AIzaSyCBIds_cFGOskS5l0Iia6gQpktlFxnZKa4",
    "AIzaSyCS9wvickFYJOFOBVRQOHXlqmJSlVfyYP4",
    "AIzaSyBFC8ivOOC-Jx1Pw-1IR2kKNZMoD7tA8-w",
    "AIzaSyBPYBqvo4we__fTR1y7OAjEdfSDygJD6Qk",
    "AIzaSyDsws9k85DheHn_DVRFYQyI__pbqm3Dh5Q",
    "AIzaSyBrMR1ZYXbm1P1VgIAVE74e3aGs88hdsgk",
    "AIzaSyAPiSP9X4fxktgwyH59wNr2VuP3bLQXWEg",
    "AIzaSyAlSBG6nDGWLw7I02Bma_68k72L8iXNXbY",
    "AIzaSyAQ4Pvci4sKNffYKODGkSHpHZb4OQExflM"
]

class AssistantQuery(BaseModel):
    command: str
    patient_id: int

@router.post("/assistant")
def ask_assistant(query: AssistantQuery):
    prompt = f"Пациент с ID {query.patient_id}. Команда: {query.command}"

    for key in API_KEYS:
        try:
            genai.configure(api_key=key)
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(prompt)
            return {"response": response.text}
        except Exception as e:
            error_msg = str(e)
            if "quota" in error_msg.lower() or "unauthorized" in error_msg.lower():
                continue
            raise HTTPException(status_code=500, detail=f"Gemini error: {error_msg}")

    raise HTTPException(status_code=503, detail="Все ключи Gemini исчерпаны или недействительны.")
