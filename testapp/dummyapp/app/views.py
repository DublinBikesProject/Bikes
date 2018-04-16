
from flask import Flask, jsonify, render_template, current_app
from sqlalchemy import create_engine
import pymysql
import simplejson as json
from pprint import pprint
from app import app

@app.route('/daily/<name>/<day>')
def get_hourly(name, day):
    engine = db_connect()
    connect = engine.connect()
    Hourly = []
    rows = connect.execute("SELECT AVG(available_bikes) as ab, AVG(available_bike_stands) as ast, hour FROM bikes WHERE address ='{}' AND dOW = '{}' GROUP BY hour".format(name, day))
    for row in rows:
        Hourly.append(dict(row))
    return jsonify(Hourly=Hourly)

@app.route('/daily/<name>')
def get_daily(name):
    engine = db_connect()
    connect = engine.connect()
    data = []
    rows = connect.execute("SELECT DOW, address, AVG(available_bikes) as ab, AVG(available_bike_stands) as ast, hour FROM bikes WHERE address ='{}' GROUP BY DOW".format(name))
    for row in rows:
        data.append(dict(row))
    return jsonify(data=data)

@app.route('/weather')
def avgWeather():
    engine = db_connect()
    connect = engine.connect()
    data = []
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

    dublin_weather = []
    historical_weather = connect.execute("SELECT avg(rain_mm)as h FROM sqlpublic.dublin_rain Where DOW = 'Monday'")
    for i in historical_weather:
        dublin_weather.append(dict(i))
    historical_weather = connect.execute("SELECT avg(rain_mm) as h FROM sqlpublic.dublin_rain Where DOW = 'Tuesday'")
    for i in historical_weather:
        dublin_weather.append(dict(i))
    historical_weather = connect.execute("SELECT avg(rain_mm) as h FROM sqlpublic.dublin_rain Where DOW = 'Wednesday'")
    for i in historical_weather:
        dublin_weather.append(dict(i))
    historical_weather = connect.execute("SELECT avg(rain_mm) as h FROM sqlpublic.dublin_rain Where DOW = 'Thursday'")
    for i in historical_weather:
        dublin_weather.append(dict(i))
    historical_weather = connect.execute("SELECT avg(rain_mm) as h FROM sqlpublic.dublin_rain Where DOW = 'Friday'")
    for i in historical_weather:
        dublin_weather.append(dict(i))
    historical_weather = connect.execute("SELECT avg(rain_mm) as h FROM sqlpublic.dublin_rain Where DOW = 'Saturday'")
    for i in historical_weather:
        dublin_weather.append(dict(i))
    historical_weather = connect.execute("SELECT avg(rain_mm) as h FROM sqlpublic.dublin_rain Where DOW = 'Sunday'")
    for i in historical_weather:
        dublin_weather.append(dict(i))
    
    jsonify(dublin_weather=dublin_weather)

    '''
    averages = []
 
    bikes = connect.execute("Select  address, avg(available_bikes) as ab, avg(available_bike_stands) as ast from bikes where DOW = 'Monday' group by address")
    for i in bikes:
        averages.append(dict(i))
    bikes = connect.execute("Select  address, avg(available_bikes) as ab, avg(available_bike_stands) as ast from bikes where DOW = 'Tuesday' group by address")
    for i in bikes:
        averages.append(dict(i))
    bikes = connect.execute("Select  address, avg(available_bikes) as ab, avg(available_bike_stands) as ast from bikes where DOW = 'Wednesday' group by address")
    for i in bikes:
        averages.append(dict(i))
    bikes = connect.execute("Select  address, avg(available_bikes) as ab, avg(available_bike_stands) as ast from bikes where DOW = 'Thursday' group by address")
    for i in bikes:
        averages.append(dict(i))
    bikes = connect.execute("Select  address, avg(available_bikes) as ab, avg(available_bike_stands) as ast from bikes where DOW = 'Friday' group by address")
    for i in bikes:
        averages.append(dict(i))
    bikes = connect.execute("Select  address, avg(available_bikes) as ab, avg(available_bike_stands) as ast from bikes where DOW = 'Saturday' group by address")
    for i in bikes:
        averages.append(dict(i))
    bikes = connect.execute("Select  address, avg(available_bikes) as ab, avg(available_bike_stands) as ast from bikes where DOW = 'Sunday' group by address")
    for i in bikes:
        averages.append(dict(i))
    
    jsonify(averages=averages)



    averages2 = []
    avg =connect.execute("select distinct address, avg(available_bikes) as ab, avg(available_bike_stands) as ast from bikes where HOUR = 6 group by address")    
    for i in avg:
        averages2.append(dict(i))
    avg =connect.execute("select distinct address, avg(available_bikes) as ab, avg(available_bike_stands) as ast from bikes where HOUR = 7 group by address")    
    for i in avg:
        averages2.append(dict(i))
    avg =connect.execute("select distinct address, avg(available_bikes) as ab, avg(available_bike_stands) as ast from bikes where HOUR = 8 group by address")    
    for i in avg:
        averages2.append(dict(i))
    avg =connect.execute("select distinct address, avg(available_bikes) as ab, avg(available_bike_stands) as ast from bikes where HOUR = 9 group by address")    
    for i in avg:
        averages2.append(dict(i))
    avg =connect.execute("select distinct address, avg(available_bikes) as ab, avg(available_bike_stands) as ast from bikes where HOUR = 10 group by address")    
    for i in avg:
        averages2.append(dict(i))
    avg =connect.execute("select distinct address, avg(available_bikes) as ab, avg(available_bike_stands) as ast from bikes where HOUR = 11 group by address")    
    for i in avg:
        averages2.append(dict(i))
    avg =connect.execute("select distinct address, avg(available_bikes) as ab, avg(available_bike_stands) as ast from bikes where HOUR = 12 group by address")    
    for i in avg:
        averages2.append(dict(i))
    avg =connect.execute("select distinct address, avg(available_bikes) as ab, avg(available_bike_stands) as ast from bikes where HOUR = 13 group by address")    
    for i in avg:
        averages2.append(dict(i))
    avg =connect.execute("select distinct address, avg(available_bikes) as ab, avg(available_bike_stands) as ast from bikes where HOUR = 14 group by address")    
    for i in avg:
        averages2.append(dict(i))
    avg =connect.execute("select distinct address, avg(available_bikes) as ab, avg(available_bike_stands) as ast from bikes where HOUR = 15 group by address")    
    for i in avg:
        averages2.append(dict(i))
    avg =connect.execute("select distinct address, avg(available_bikes) as ab, avg(available_bike_stands) as ast from bikes where HOUR = 16 group by address")    
    for i in avg:
        averages2.append(dict(i))
    avg =connect.execute("select distinct address, avg(available_bikes) as ab, avg(available_bike_stands) as ast from bikes where HOUR = 17 group by address")    
    for i in avg:
        averages2.append(dict(i))
    avg =connect.execute("select distinct address, avg(available_bikes) as ab, avg(available_bike_stands) as ast from bikes where HOUR = 18 group by address")    
    for i in avg:
        averages2.append(dict(i))
    avg =connect.execute("select distinct address, avg(available_bikes) as ab, avg(available_bike_stands) as ast from bikes where HOUR = 19 group by address")    
    for i in avg:
        averages2.append(dict(i))
    avg =connect.execute("select distinct address, avg(available_bikes) as ab, avg(available_bike_stands) as ast from bikes where  HOUR = 20 group by address")    
    for i in avg:
        averages2.append(dict(i))
    avg =connect.execute("select distinct address, avg(available_bikes) as ab, avg(available_bike_stands) as ast from bikes where HOUR = 21 group by address")    
    for i in avg:
        averages2.append(dict(i))
    avg =connect.execute("select distinct address, avg(available_bikes) as ab, avg(available_bike_stands) as ast from bikes where HOUR = 22 group by address")    
    for i in avg:
        averages2.append(dict(i))
    avg =connect.execute("select distinct address, avg(available_bikes) as ab, avg(available_bike_stands) as ast from bikes where HOUR = 23 group by address")    
    for i in avg:
        averages2.append(dict(i))
    
    jsonify(averages2=averages2)'''
    
    return render_template("index.html", data=points, weather=weather,dublin_weather=dublin_weather)
