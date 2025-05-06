from flask import Flask, render_template, request, redirect, session, g
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# MODELE
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)

class Plant(db.Model):
    __tablename__ = 'plants'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(100), nullable=False)
    watering_day = db.Column(db.String(20))
    watering_time = db.Column(db.String(20))
    photo_url = db.Column(db.String(300))

# Ładowanie użytkownika z sesji
@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    g.user = User.query.get(user_id) if user_id else None

# LOGIN
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect('/dashboard')
        return 'Błędny login lub hasło'
    return render_template('login.html')

# REJESTRACJA
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(email=email).first():
            return "Użytkownik już istnieje"
        hashed_password = generate_password_hash(password)
        db.session.add(User(email=email, password=hashed_password))
        db.session.commit()
        return redirect('/')
    return render_template('register.html')

# WYLOGOWANIE
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

# DASHBOARD
@app.route('/dashboard')
def dashboard():
    if not g.user:
        return redirect('/')
    plants = Plant.query.filter_by(user_id=g.user.id).all()
    return render_template('dashboard.html', plants=plants)

# DODAWANIE ROŚLINY
@app.route('/add_plant', methods=['POST'])
def add_plant():
    if not g.user:
        return redirect('/')
    plant = Plant(
        user_id=g.user.id,
        name=request.form['name'],
        watering_day=request.form['watering_day'],
        watering_time=request.form['watering_time'],
        photo_url=request.form['photo_url']
    )
    db.session.add(plant)
    db.session.commit()
    return redirect('/dashboard')

# USUWANIE ROŚLINY
@app.route('/delete_plant/<int:plant_id>', methods=['POST'])
def delete_plant(plant_id):
    if not g.user:
        return redirect('/')
    plant = Plant.query.get_or_404(plant_id)
    if plant.user_id != g.user.id:
        return "Brak dostępu"
    db.session.delete(plant)
    db.session.commit()
    return redirect('/dashboard')

# FORMULARZ EDYCJI ROŚLINY
@app.route('/edit_plant/<int:plant_id>', methods=['GET', 'POST'])
def edit_plant(plant_id):
    if not g.user:
        return redirect('/')
    plant = Plant.query.get_or_404(plant_id)
    if plant.user_id != g.user.id:
        return "Brak dostępu"

    if request.method == 'POST':
        plant.name = request.form['name']
        plant.watering_day = request.form['watering_day']
        plant.watering_time = request.form['watering_time']
        plant.photo_url = request.form['photo_url']
        db.session.commit()
        return redirect('/dashboard')

    return render_template('edit_plant.html', plant=plant)

# TWORZENIE TABEL
with app.app_context():
    db.create_all()

# URUCHOMIENIE
if __name__ == '__main__':
    app.run(debug=True)
