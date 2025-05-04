
from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'tajny_klucz'  # zmień na bezpieczny w praktyce

# Prosty użytkownik w pamięci (zamiast bazy danych)
users = {'admin': generate_password_hash('haslo123')}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            return redirect('/dashboard')
        else:
            return 'Błędne dane logowania'
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/')
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)

