from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth import require_roles, get_current_user
from app.models import Test, Question, Answer, UserResult, User
from app.database import get_db
from app.schemas import TestCreate, QuestionCreate, AnswerCreate, TestSubmission
from datetime import datetime

router = APIRouter()

@router.post("/tests")
def create_test(test: TestCreate, db: Session = Depends(get_db), current_user = Depends(require_roles("admin"))):
    new_test = Test(name=test.name)
    db.add(new_test)
    db.flush()
    for q in test.questions:
        question = Question(text=q.text, test_id=new_test.id)
        db.add(question)
        db.flush()
        for a in q.answers:
            db.add(Answer(text=a.text, is_correct=a.is_correct, question_id=question.id))
    db.commit()
    return {"message": "Тест создан"}

@router.get("/tests")
def get_tests(db: Session = Depends(get_db)):
    return db.query(Test).all()

@router.post("/tests/{test_id}/submit")
def submit_test(test_id: int, submission: TestSubmission, db: Session = Depends(get_db), current_user: User = Depends(require_roles("doctor", "registrar"))):
    score = 0
    for item in submission.answers:
        correct = db.query(Answer).filter_by(question_id=item.question_id, is_correct=True).all()
        submitted_ids = set(item.selected_answer_ids)
        correct_ids = set(a.id for a in correct)
        if submitted_ids == correct_ids:
            score += 1

    result = UserResult(user_id=current_user.id, test_id=test_id, score=score, submitted_at=datetime.utcnow())
    db.add(result)
    db.commit()
    return {"score": score}

@router.get("/results/me")
def my_results(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(UserResult).filter(UserResult.user_id == current_user.id).all()

@router.get("/results/all")
def all_results(db: Session = Depends(get_db), current_user = Depends(require_roles("admin"))):
    return db.query(UserResult).all()
