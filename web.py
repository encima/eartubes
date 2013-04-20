from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import json
import sqlite3

DEBUG = True
DATABASE = 'data.db'
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/')
def index():
    if 'id' in session:
        return render_template('dashboard.html')
    else:
        return render_template('login.html')

#partial search for movies from sqlite
@app.route('/ps', methods=['GET'])
def movie_search():
    term = request.args.get('q')
    cur = g.db.execute("SELECT id, title FROM movies WHERE UPPER(title) LIKE UPPER('%" + term  + "%');")
    #convert sql result to json and return
    entries = [dict(id=row[0], title=row[1]) for row in cur.fetchall()]
    print entries
    return json.dumps(entries)

@app.route('/register/', methods=['POST'])
def register():
    error = None

@app.route('/login/', methods=['POST'])
def login():
    error = None
    if request.form['email'] != USERNAME:
        error = 'Invalid username'
    elif request.form['password'] != PASSWORD:
        error = 'Invalid password'
    else:
        session['id'] = 12345
        return json.dumps({'success':True})
    return json.dumps({'success':False, 'error':error})

@app.route('/logout')
def logout():
    session.pop('id', None)
    flash('You were logged out')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
