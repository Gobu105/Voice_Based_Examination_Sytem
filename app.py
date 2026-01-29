from flask import Flask, render_template, request, redirect, url_for, session
from models import db

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = USERS.get(username)

        if user and user["password"] == password:
            session['username'] = username
            session['role'] = user["role"]

            if user["role"] == "student":
                return redirect(url_for('student_dashboard'))
            elif user["role"] == "invigilator":
                return redirect(url_for('invigilator_dashboard'))
            elif user["role"] == "admin":
                return redirect(url_for('admin_dashboard'))
        else:
            error = "Invalid credentials"

    return render_template('login.html', error=error)

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
