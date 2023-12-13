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
        is_manager = form.manager_code.data == '3182'  # Check manager code

        db = get_db()
        db.execute('INSERT INTO user (username, password, is_manager) VALUES (?, ?, ?)',
                   (username, password, is_manager))
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
            session['is_manager'] = user['is_manager'] == 1  # Store manager status
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.')

    return render_template('login.html', form=form)
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/tracker', methods=['GET', 'POST'])
def tracker():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        date = request.form['date']
        task_name = request.form['task_name']
        start_time = request.form['start_time']
        end_time = request.form['end_time']

        db = get_db()
        db.execute('INSERT INTO time_entry (user_id, date, task_name, start_time, end_time) VALUES (?, ?, ?, ?, ?)',
                   (session['user_id'], date, task_name, start_time, end_time))
        db.commit()
        close_db()

    db = get_db()
    entries = db.execute('SELECT * FROM time_entry WHERE user_id = ?', (session['user_id'],)).fetchall()
    close_db()

    return render_template('tracker.html', entries=entries)

@app.route('/usernames')
def show_usernames():
    if 'user_id' not in session or not session.get('is_manager'):
        flash('You must be a manager to view this page.')
        return redirect(url_for('login'))

    db = get_db()
    manager_usernames = db.execute('SELECT username FROM user WHERE is_manager = TRUE').fetchall()
    normal_usernames = db.execute('SELECT username FROM user WHERE is_manager = FALSE').fetchall()
    close_db()

    return render_template('usernames.html', manager_usernames=manager_usernames, normal_usernames=normal_usernames)


if __name__ == '__main__':
    app.run(debug=True)