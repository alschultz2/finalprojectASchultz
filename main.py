from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db, close_db
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=('GET', 'POST'))
def register():
    print("Register route accessed")  # Debug print

    form = RegistrationForm(request.form)
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            password = generate_password_hash(form.password.data)

            print(f"Attempting to register user: {username}")  # Debug print

            try:
                db = get_db()
                db.execute('INSERT INTO user (username, password) VALUES (?, ?)', (username, password))
                db.commit()

                print(f"User {username} registered successfully")  # Debug print
            except Exception as e:
                print("An error occurred during registration:", e)  # Debug print
            finally:
                close_db()

            return redirect(url_for('login'))
        else:
            print("Form validation failed")  # Debug print

    return render_template('register.html', form=form)

@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data

        db = get_db()
        user = db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()
        close_db()

        if user and check_password_hash(user['password'], password):
            return redirect(url_for('home'))

    return render_template('login.html', form=form)

@app.route('/usernames')
def show_usernames():
    db = get_db()
    usernames = db.execute('SELECT username FROM user').fetchall()
    close_db()
    return render_template('usernames.html', usernames=usernames)

if __name__ == '__main__':
    app.run(debug=True)
