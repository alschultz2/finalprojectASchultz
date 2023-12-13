from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db, close_db
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('home'))

    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = generate_password_hash(form.password.data)

        db = get_db()
        db.execute('INSERT INTO user (username, password) VALUES (?, ?)', (username, password))
        db.commit()
        close_db()

        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('home'))

    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data

        db = get_db()
        user = db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()
        close_db()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/tracker')
def tracker():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Placeholder for time tracker page logic
    return render_template('tracker.html')

@app.route('/usernames')
def show_usernames():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db()
    usernames = db.execute('SELECT username FROM user').fetchall()
    close_db()

    return render_template('usernames.html', usernames=usernames)

if __name__ == '__main__':
    app.run(debug=True)
