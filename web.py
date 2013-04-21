from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import json
import urllib
import sqlite3
import re
import MySQLdb as mdb
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
    connection = mdb.connect(user="root",passwd="",db="imdb",host="eartub.es", charset="utf8")
    cursor = connection.cursor(mdb.cursors.DictCursor)
    return cursor
    # return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/')
def index():
    if 'id' in session:
        if 'lastfm_username' in session:
            lastfm_user = session['lastfm_username']
            lastfm = True
        else: 
            lastfm_user = None
            lastfm = False
        return render_template('dashboard.html', lastfm_username = lastfm_user, lastfm_enabled = lastfm)
    else:
        return render_template('login.html')

#partial search for movies from sqlite
@app.route('/api/ps', methods=['POST'])
def movie_search():
    term = request.form['q']
    term = term.replace("'", "")
    # query = "SELECT id, title, year FROM movies WHERE UPPER(title) LIKE UPPER(\"%" + term  + "%\") LIMIT 10;"
    query = "SELECT id, title, production_year AS year FROM title WHERE UPPER(title) LIKE UPPER(\"%" + term  + "%\") AND kind_id=1 LIMIT 10;" 
    cur = g.db.execute(query)
    #convert sql result to json and return
    #entries = [dict(id=row[0], title=row[1], year=row[2]) for row in cur.fetchall()]
    resp = g.db.fetchall()
    return json.dumps(resp)

@app.route('/api/tk', methods=['POST'])
def tastekid_search():
    term = request.form['q']
    term = term.replace("'", "")
    response = json.loads(tk.get_similar_movies(term))
    return json.dumps(response)

@app.route('/api/imdb', methods=['POST'])
def imdb_search():
    term = request.form['q']
    term = urllib.url2pathname(term)
    term = term.replace("'", "")
    print term
    response = json.loads(ia.get_info(movie=term))
    print response
    if len(response) is 1:
        poster = None
        if 'poster' in response[0].keys():
            poster =  response[0]['poster']
        title =  response[0]['title']
        term = title.replace("'", "")
        imdb_id = response[0]['imdb_id']
        year = response[0]['year']
        query = "SELECT id FROM title WHERE UPPER(title) LIKE UPPER(\"%" + term  + "%\") AND production_year=" + str(year) + " AND kind_id=1;"
        cur = g.db.execute(query)
        result = g.db.fetchone()
        query = "UPDATE title SET imdb_id=\"" + str(imdb_id) + "\", poster=\"" + str(poster) + "\" WHERE id=" + str(result['id']) + ";"
        print query
        g.db.execute(query)
        return json.dumps(response)
    else:
        return "{Error: No Results}"

def get_films_by(id, start, limit):
    query = ""
    cur = g.db.execute(query)
    result = g.db.fetchall()
    return json.dumps(result)

@app.route('/lastfm_auth/')
def lastfm_auth():
    handler = LastFMHandler()
    return redirect(handler.get_request_auth())

@app.route('/lastfm_caller')
def lastfm_callback():
    handler = LastFMHandler()
    info = handler.authenticate_service(request)
    lastfm_key = info[0]
    lastfm_username = info[1]
    session['lastfm_key'] = lastfm_key
    session['lastfm_username'] = lastfm_username
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
    app.run(host='0.0.0.0')
