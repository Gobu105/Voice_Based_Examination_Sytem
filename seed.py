from app import app
from models import db, Registration, Candidate, Exam, Question
from werkzeug.security import generate_password_hash, check_password_hash


with app.app_context():

    # -----------------------------
    # INVIGILATOR
    # -----------------------------
    invigilator = Registration(
        full_name="Exam Invigilator",
        username="invigilator1",
        email="invigilator@example.com",
        password_hash=generate_password_hash("invigilator_pass"),
        role="INVIGILATOR"
    )
    db.session.add(invigilator)
    db.session.commit()

    # -----------------------------
    # CANDIDATE
    # -----------------------------
    candidate_user = Registration(
        full_name="Test Candidate",
        username="candidate1",
        email="candidate@example.com",
        password_hash="hashed_password",
        role="CANDIDATE",
        phone_no="8888888888"
    )
    db.session.add(candidate_user)
    db.session.commit()

    candidate = Candidate(
        reg_id=candidate_user.reg_id,
        registration_no="CAND-001"
    )
    db.session.add(candidate)
    db.session.commit()

    # -----------------------------
    # EXAM
    # -----------------------------
    exam = Exam(
        exam_name="Sample Voice Exam",
        duration=30,
        total_marks=100,
        created_by=invigilator.reg_id
    )
    db.session.add(exam)
    db.session.commit()

    # -----------------------------
    # QUESTIONS
    # -----------------------------
    questions = [
        Question(exam_id=exam.exam_id, question_text="What is photosynthesis?"),
        Question(exam_id=exam.exam_id, question_text="Define computer network."),
        Question(exam_id=exam.exam_id, question_text="Explain the concept of operating systems.")
    ]

    db.session.add_all(questions)
    db.session.commit()

    print("Database seeded successfully!")