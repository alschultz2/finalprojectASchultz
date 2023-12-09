from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register')
def register():
    return 'Register Page'

@app.route('/login')
def login():
    return 'Login Page'

@app.route('/tracker')
def tracker():
    return 'Time Tracker Page'

if __name__ == '__main__':
    app.run(debug=True)
