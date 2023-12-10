from flask import Flask, render_template, request, redirect, url_for
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
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = generate_password_hash(form.password.data)

        db = get_db()
        db.execute('INSERT INTO user (username, password) VALUES (?, ?)', (username, password))
        db.commit()
        close_db()

        return redirect(url_for('login'))

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

if __name__ == '__main__':
    app.run(debug=True)
