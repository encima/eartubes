from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import json
import urllib2
import sqlite3
from api.imdb_api import IMDBApi
from api.tastekid_api import TastekidApi
from api.lastfm_handler import LastFMHandler 

DEBUG = True
DATABASE = 'data.db'
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
tk, ia= TastekidApi(), IMDBApi()

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
@app.route('/api/ps', methods=['GET'])
def movie_search():
    term = request.args.get('q')
    cur = g.db.execute("SELECT id, title, year FROM movies WHERE UPPER(title) LIKE UPPER('%" + term  + "%');")
    #convert sql result to json and return
    entries = [dict(id=row[0], title=row[1], year=row[2]) for row in cur.fetchall()]
    print entries
    return json.dumps(entries)

@app.route('/api/tk', methods=['GET'])
def tastekid_search():
    term = request.args.get('q')
    response = json.loads(tk.get_similar_movies_from_artists(term))
    print response
    return json.dumps(response)

@app.route('/api/imdb', methods=['GET'])
def imdb_search():
    term = request.args.get('q')
    term = urllib.url2pathname(term)
    print term
    response = json.loads(ia.get_info(movie=term))
    print response
    if len(response) is 1:
        if 'poster' in response[0].keys():
            poster =  response[0]['poster']
        title =  response[0]['title']
        imdb_id = response[0]['imdb_id']
        cur = g.db.execute("SELECT id FROM movies WHERE UPPER(title) LIKE UPPER('%" + title  + "%');")

        return json.dumps(response)
    else:
        return "{Error: No Results}"

@app.route('/lastfm_auth/')
def lastfm_auth():
    return "auth string (from api)"

@app.route('/lastfm_callback')
def lastfm_callback():
    # call lastfm method for callback stuff
    return redirect(url_for('index'))

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

@app.route('/logout/')
def logout():
    session.pop('id', None)
    flash('You were logged out')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
