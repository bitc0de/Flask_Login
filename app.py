from flask import Flask, render_template, request, url_for, redirect, session, flash
from functools import wraps

app = Flask(__name__)
app.secret_key = "mysecretkey"

# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/welcome')
@login_required
def welcome ():
    return render_template('welcome.html')

@app.route ('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin': #admin/admin is user and password. Change this!
            error = 'Invalid credentials. Please try again'
        else:
            session['logged_in'] = True
            flash ('you were just logged in!')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route ('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('welcome'))

if __name__ == '__main__':
    app.run(debug=True)
