import pickle
import pandas as pd
import datetime as dt
from flask import Flask, jsonify, render_template, current_app
from sqlalchemy import create_engine
import pymysql
import simplejson as json
from pprint import pprint
from app import app
import os
import numpy as np

@app.route('/predict/<station>')
def predict_bikes(station):

    rain_forecast = {"x":"y"}
    engine = create_engine("mysql+pymysql://publicdb:sqlpublic@52.43.48.163:3306/sqlpublic",echo=False)
    connection = engine.connect()
    trans = connection.begin()
    rows = connection.execute("SELECT round(threeH_rain_predict * 100) as rain FROM weather")
    trans.commit()
    for i in rows:
        rain_forecast.update(dict(i))
    
    path = './app/stations/'
    os.makedirs(path, exist_ok=True) #create directory when non-existing
    
    if station == "Princes Street / O'Connell Street": # to handle the slash in the station name
        station = "Princes Street O'Connell Street"
        
        
    address = station+'.pkl'
    day = dt.datetime.today().weekday() # current day of the week 0=Monday
    hour = (dt.datetime.now().hour) +3 # current hour + 3
    rain = rain_forecast['rain'] # can use an sql query to get this

    # SELECT round(threeH_rain_predict * 100) FROM weather;

    with open(path+address,'rb') as input:
        rfc = pickle.load(input)

    df = pd.DataFrame({'HOUR': [hour],  'rain_in_mm': [rain]})
    df_dummies_DOW = pd.DataFrame({'DOW_Monday': [1], 'DOW_Tuesday': [0],'DOW_Wednesday': [0], 'DOW_Thursday': [0],'DOW_Friday': [0], 'DOW_Saturday': [0],'DOW_Sunday': [0]})

    if day == 0:
        df_dummies_DOW = pd.DataFrame({'DOW_Monday': [1], 'DOW_Tuesday': [0],'DOW_Wednesday': [0], 'DOW_Thursday': [0],'DOW_Friday': [0], 'DOW_Saturday': [0],'DOW_Sunday': [0]})
    elif day == 1:
        df_dummies_DOW = pd.DataFrame({'DOW_Monday': [0], 'DOW_Tuesday': [1],'DOW_Wednesday': [0], 'DOW_Thursday': [0],'DOW_Friday': [0], 'DOW_Saturday': [0],'DOW_Sunday': [0]})
    elif day == 2:
        df_dummies_DOW = pd.DataFrame({'DOW_Monday': [0], 'DOW_Tuesday': [0],'DOW_Wednesday': [1], 'DOW_Thursday': [0],'DOW_Friday': [0], 'DOW_Saturday': [0],'DOW_Sunday': [0]})
    elif day == 3:
        df_dummies_DOW = pd.DataFrame({'DOW_Monday': [0], 'DOW_Tuesday': [0],'DOW_Wednesday': [0], 'DOW_Thursday': [1],'DOW_Friday': [0], 'DOW_Saturday': [0],'DOW_Sunday': [0]})
    elif day == 4:
        df_dummies_DOW = pd.DataFrame({'DOW_Monday': [0], 'DOW_Tuesday': [0],'DOW_Wednesday': [0], 'DOW_Thursday': [0],'DOW_Friday': [1], 'DOW_Saturday': [0],'DOW_Sunday': [0]})
    elif day == 5:
        df_dummies_DOW = pd.DataFrame({'DOW_Monday': [0], 'DOW_Tuesday': [0],'DOW_Wednesday': [0], 'DOW_Thursday': [0],'DOW_Friday': [0], 'DOW_Saturday': [1],'DOW_Sunday': [0]})
    else:
        df_dummies_DOW = pd.DataFrame({'DOW_Monday': [0], 'DOW_Tuesday': [0],'DOW_Wednesday': [0], 'DOW_Thursday': [0],'DOW_Friday': [0], 'DOW_Saturday': [0],'DOW_Sunday': [1]})

    df_cont_feat = df[['HOUR','rain_in_mm']]
    X = pd.concat([df_cont_feat, df_dummies_DOW[['DOW_Monday', 'DOW_Tuesday','DOW_Wednesday', 'DOW_Thursday','DOW_Friday', 'DOW_Saturday','DOW_Sunday']]], axis =1)

    return str(rfc.predict(X))


@app.route('/hourly/<path:name>/<day>')
def get_hourly(name, day):
    print(name)
    name = name.replace("'","''")
    engine = db_connect()
    connect = engine.connect()
    Hourly = []
    rows = connect.execute("SELECT AVG(available_bikes) as ab, AVG(available_bike_stands) as ast, hour FROM bikes WHERE address ='{}' AND dOW = '{}' GROUP BY hour".format(name, day))
    for row in rows:
        Hourly.append(dict(row))
    rows = connect.execute("SELECT HOUR, DOW, avg(rain_in_mm) as r FROM sqlpublic.dublin_hourly_rain WHERE DOW = '{}' Group by HOUR;".format(day))
    for row in rows:
        Hourly.append(dict(row))
    return jsonify(Hourly=Hourly)

@app.route('/daily/<path:name>')
def get_daily(name):
    print(name)
    name = name.replace("'","''")
    engine = db_connect()
    connect = engine.connect()
    data = []
    rows = connect.execute("SELECT DOW, address, AVG(available_bikes) as ab, AVG(available_bike_stands) as ast, hour FROM bikes WHERE address ='{}' GROUP BY DOW".format(name))
    for row in rows:
        data.append(dict(row))
    rows = connect.execute("SELECT DOW, avg(rain_mm)as r FROM sqlpublic.dublin_rain GROUP BY DOW;")
    for row in rows:
        data.append(dict(row))
    return jsonify(data=data)

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
    rows = connect.execute("select * from bikes where last_update in (select max(last_update) from bikes group by address);")
    for row in rows:
        points.append(dict(row))
    jsonify(points=points)
    
    weather = []
    info = connect.execute("SELECT * FROM weather")
    for i in info:
        weather.append(dict(i))
    jsonify(weather=weather)

     
    return render_template("index.html", data=points, weather=weather) 