from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# -----------------------------
# REGISTRATION
# -----------------------------
class Registration(db.Model):
    __tablename__ = 'registration'

    reg_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('INVIGILATOR', 'CANDIDATE', name='user_roles'), nullable=False)
    phone_no = db.Column(db.String(15))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    login = db.relationship('Login', backref='registration', uselist=False)
    candidate = db.relationship('Candidate', backref='registration', uselist=False)
    exams = db.relationship('Exam', backref='invigilator')


# -----------------------------
# LOGIN
# -----------------------------
class Login(db.Model):
    __tablename__ = 'login'

    login_id = db.Column(db.Integer, primary_key=True)
    reg_id = db.Column(db.Integer, db.ForeignKey('registration.reg_id'), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    last_login = db.Column(db.DateTime)


# -----------------------------
# CANDIDATES
# -----------------------------
class Candidate(db.Model):
    __tablename__ = 'candidates'

    candidate_id = db.Column(db.Integer, primary_key=True)
    reg_id = db.Column(db.Integer, db.ForeignKey('registration.reg_id'), nullable=False)
    registration_no = db.Column(db.String(50), unique=True, nullable=False)

    exam_sessions = db.relationship('ExamSession', backref='candidate')


# -----------------------------
# EXAMS
# -----------------------------
class Exam(db.Model):
    __tablename__ = 'exams'

    exam_id = db.Column(db.Integer, primary_key=True)
    exam_name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    total_marks = db.Column(db.Integer)
    created_by = db.Column(db.Integer, db.ForeignKey('registration.reg_id'), nullable=False)

    questions = db.relationship('Question', backref='exam')
    sessions = db.relationship('ExamSession', backref='exam')


# -----------------------------
# QUESTIONS
# -----------------------------
class Question(db.Model):
    __tablename__ = 'questions'

    question_id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.exam_id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)

    answers = db.relationship('Answer', backref='question')


# -----------------------------
# EXAM SESSIONS
# -----------------------------
class ExamSession(db.Model):
    __tablename__ = 'exam_sessions'

    session_id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.exam_id'), nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.candidate_id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    status = db.Column(
        db.Enum('STARTED', 'SUBMITTED', 'ENDED', name='session_status'),
        default='STARTED'
    )

    answers = db.relationship('Answer', backref='session')


# -----------------------------
# ANSWERS
# -----------------------------
class Answer(db.Model):
    __tablename__ = 'answers'

    answer_id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('exam_sessions.session_id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.question_id'), nullable=False)
    answer_text = db.Column(db.Text, nullable=False)

    evaluation = db.relationship('Evaluation', backref='answer', uselist=False)


# -----------------------------
# EVALUATIONS
# -----------------------------
class Evaluation(db.Model):
    __tablename__ = 'evaluations'

    evaluation_id = db.Column(db.Integer, primary_key=True)
    answer_id = db.Column(db.Integer, db.ForeignKey('answers.answer_id'), unique=True, nullable=False)
    marks_awarded = db.Column(db.Integer)
    evaluated_by = db.Column(db.Integer, db.ForeignKey('registration.reg_id'))