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
    connection = mdb.connect(user="root",passwd="",db="imdb",host="localhost", charset="utf8")
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
            lastfm_username = session['lastfm_username']
            lastfm = True
        else: 
            lastfm_username = None
            lastfm = False
        return render_template('dashboard.html', lastfm_username = lastfm_username, lastfm = lastfm)
    else:
        return render_template('login.html')

#partial search for movies from sqlite
@app.route('/api/ps', methods=['POST'])
def movie_search():
    term = request.form['q']
    term = term.replace("'", "")
    # query = "SELECT id, title, year FROM movies WHERE UPPER(title) LIKE UPPER(\"%" + term  + "%\") LIMIT 10;"
    query = "(SELECT id, title, production_year AS year FROM title WHERE UPPER(title) LIKE UPPER(\"" + term  + "\") AND kind_id=1 LIMIT 5) UNION ALL (SELECT id, title, production_year AS year FROM title WHERE UPPER(title) LIKE UPPER(\"%" + term  + "%\") AND kind_id=1 LIMIT 5);" 
    cur = g.db.execute(query)
    #convert sql result to json and return
    #entries = [dict(id=row[0], title=row[1], year=row[2]) for row in cur.fetchall()]
    resp = g.db.fetchall()
    return json.dumps(resp)

@app.route('/api/tk', methods=['POST'])
def tastekid_search():
    term = request.form['q']
    term = term.replace("'", "")
    response = json.loads(tk.get_similar_movies_from_artists(term))
    return json.dumps(response)

@app.route('/api/imdb', methods=['POST'])
def imdb_search():
    term = request.form['q']
    term = urllib.url2pathname(term)
    term = term.replace("'", "")
    response = json.loads(ia.get_info(movie=term))
    if len(response) is 1:
        if 'poster' in response[0].keys():
            poster =  response[0]['poster']
        title =  response[0]['title']
        term = title.replace("'", "")
        imdb_id = response[0]['imdb_id']
        year = response[0]['year']
        #cur = g.db.cursor()
        cur = g.db.execute("SELECT id FROM title WHERE UPPER(title) LIKE UPPER(\"%" + term  + "%\") AND production_year=" + year + " AND kind_id=1;")
        # result = cur.execute("SELECT id FROM movies WHERE UPPER(title) LIKE UPPER('%" + term  + "%');").fetchone()
        result = g.db.fetchone()
        query = "UPDATE title SET imdb_id=\"" + imdb_id + "\", poster=\"" + poster + "\" WHERE id=" + result['id'] + ";"
        print query
        return json.dumps(response)
    else:
        return "{Error: No Results}"

@app.route('/lastfm_auth/')
def lastfm_auth():
    handler = LastFMHandler()
    return redirect(handler.get_request_auth())

@app.route('/lastfm_callback')
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
