import uuid
from flask import Flask
from flask import make_response, render_template, redirect
from flask import request
import sqlite3

app = Flask(__name__)

ROT_OFFSET = 20

conn = sqlite3.connect('database.db')
conn.execute('CREATE TABLE IF NOT EXISTS bin_data (id TEXT, data TEXT)')    

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        response = make_response(render_template('bin.html.template'), 200)
    elif request.method == 'POST':
        bin_id = uuid.uuid4()
        # this isn't secure
        _add_bin(bin_id, request.form['data'])
        response = redirect('/bin/' + str(bin_id), code=302)

    else:
        response = make_response(render_template('error.html.template'), 404)

    return response

@app.route("/bin/<uuid:bin_id>", methods=['GET', 'POST', 'DELETE'])
def bin(bin_id):
    if request.method == 'GET':
        data = _get_bin(bin_id)
        if data is not None:
            response = make_response(render_template('bin.html.template', data=data), 200)
        else:
            response = make_response(render_template('error.html.template'), 404)
            
    elif request.method == 'POST':
        # data should be sanitized
        data = request.form['data']
        _update_bin(bin_id, data)
        response = make_response(render_template('bin.html.template', data=data), 200)

    elif request.method == 'DELETE':
        my_dict.pop(bin_id, None)
        response = redirect('/', code=302)

    else:
        response = make_response(render_template('error.html.template'), 404)

    return response

@app.route("/encrypted/<uuid:bin_id>", methods=['GET'])
def encrypted(bin_id):
    data = _get_bin(bin_id)
    if data is not None:
        response = _encrypt(data)
    else:
        response = make_response(render_template('error.html.template'), 404)

    return response


# NOT FOR PRODUCTION 
# there's probably an issue blindly shifting ascii values but this is just for fun
def _encrypt(data):
    encrypted = ''

    for letter in data:
        encrypted += chr(ord(letter) + ROT_OFFSET % 128)

    return encrypted


def _add_bin(id, data):
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO bin_data (id, data) VALUES ('%s', '%s')" % (id, data))
        con.commit()

def _update_bin(id, data):
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE bin_data SET data = '%s' WHERE id = '%s'" % (id, data))
        con.commit()

def _get_bin(id):
    rows = None
    with sqlite3.connect("database.db") as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        
        cur.execute("SELECT data from bin_data WHERE id = '%s'" % (id))

        rows = cur.fetchall()

    if len(rows) == 0:
        return None
    else:
        return rows[0]['data']
