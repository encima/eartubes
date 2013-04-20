from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import json

DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def index():
    if 'id' in session:
        return render_template('dashboard.html')
    else:
        return render_template('login.html')

@app.route('/register/', methods=['POST'])
def register():
    error = None
    

@app.route('/login/', methods=['POST'])
def login():
    error = None
    if request.form['username'] != USERNAME:
        error = 'Invalid username'
    elif request.form['password'] != PASSWORD:
        error = 'Invalid password'
    else:
        session['id'] = 12345
        return json.dumps({'success':True})
    return json.dumps({'success':False, 'error':error})

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
