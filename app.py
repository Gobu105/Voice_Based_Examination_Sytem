from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, Registration
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = "secretkey123"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exam.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Dummy users (for prototype)
USERS = {
    "student1": {"password": "123", "role": "student"},
    "invigilator1": {"password": "123", "role": "invigilator"},
    "admin1": {"password": "123", "role": "admin"}
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = Registration.query.filter_by(username=username).first()

    # User does not exist
    if not user:
        flash("Invalid username or password")
        return redirect(url_for('home'))

    # Password does not match
    if not check_password_hash(user.password_hash, password):
        flash("Invalid username or password")
        return redirect(url_for('home'))

    # Login success
    session['user_id'] = user.reg_id
    session['role'] = user.role

    if user.role == 'INVIGILATOR':
        return redirect('/invigilator/dashboard')
    else:
        return redirect('/candidate/dashboard')

@app.route('/candidate/dashboard')
def candidate_dashboard():
    if 'user_id' not in session or session.get('role') != 'CANDIDATE':
        return redirect(url_for('home'))

    return "Candidate Dashboard"

@app.route('/invigilator/dashboard')
def invigilator_dashboard():
    if 'user_id' not in session or session.get('role') != 'INVIGILATOR':
        return redirect(url_for('home'))

    return "Invigilator Dashboard" 

@app.route('/student')
def student_dashboard():
    return render_template('student_dashboard.html')

@app.route('/invigilator')
def invigilator_dashboard():
    return render_template('invigilator_dashboard.html')

@app.route('/admin')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
