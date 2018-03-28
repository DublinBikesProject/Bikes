from flask import Flask, jsonify, render_template, current_app
from sqlalchemy import create_engine
import pymysql
import simplejson as json
from pprint import pprint
from app import app

#turn my qery intot this format
#pass with flask to html
#our_json = "var data = {BarrowStreet:{lat:53.3417,lng:-6.2362},BensonStreet:{lat:53.3442,lng:-6.23345}}"

"""def test_connection(self):
    with app.app_context():
        print(current_app.name)"""

@app.route("/locs")
def get_locs():
    #print("1")
    engine = db_connect()
    connect = engine.connect()
    locs = []
    rows = connect.execute("SELECT address,lat,lng FROM bikes;")
    #print("connected")
    for row in rows:
        locs.append(dict(row))
    return jsonify(locs=locs)

def db_connect():
    engine = create_engine("mysql+pymysql://publicdb:sqlpublic@52.43.48.163:3306/sqlpublic",echo=False)
    return engine

#our_json = get_locs()

@app.route('/')
def index():
    engine = db_connect()
    connect = engine.connect()
    locs = []
    rows = connect.execute("SELECT address,lat,lng FROM static_bikes WHERE address = 'Benson Street';")
    #print("connected")
    for row in rows:
        locs.append(dict(row))
    jsonify(locs=locs)
    return render_template("index.html", Fdata=locs)

