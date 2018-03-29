from flask import Flask, jsonify, render_template, current_app
from sqlalchemy import create_engine
import pymysql
import simplejson as json
from pprint import pprint
from app import app

@app.route("/locs")
def get_locs():
    #print("1")
    engine = db_connect()
    connect = engine.connect()
    locs = []
    rows = connect.execute("SELECT address,lat,lng FROM bikes;")
    for row in rows:
        locs.append(dict(row))
    return jsonify(locs=locs)

def db_connect():
    engine = create_engine("mysql+pymysql://publicdb:sqlpublic@52.43.48.163:3306/sqlpublic",echo=False)
    return engine

@app.route('/')
def index():
    engine = db_connect()
    connect = engine.connect()
    points = []
    #rows = connect.execute("SELECT address,lat,lng FROM static_bikes;")
    rows = connect.execute("SELECT distinct address,last_update,available_bike_stands,lat,lng,available_bikes, status, banking FROM bikes s1 WHERE last_update = (SELECT MAX(last_update) FROM bikes s2 WHERE s1.address = s2.address)GROUP BY address;")
    for row in rows:
        points.append(dict(row))
    jsonify(points=points)
    return render_template("index.html", data=points)