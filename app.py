from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Wczytaj DATABASE_URL z .env (lub ustaw bezpośrednio)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'  # 🔧 WAŻNE: ustaw nazwę tabeli jawnie
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        
        if User.query.filter_by(email=email).first():
            return "Użytkownik już istnieje"

        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        return redirect('/dashboard')  # albo strona z roślinami
    return 'Błędny login lub hasło'

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    return 'Zalogowany! Tu będzie dashboard z roślinami.'

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

# Tworzenie tabel przy starcie aplikacji
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
