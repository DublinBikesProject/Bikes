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
    historical_weather = connect.execute("SELECT avg(humidity)as h FROM sqlpublic.dublin_weather Where DOW = 'Monday'")
    for i in historical_weather:
        dublin_weather.append(dict(i))
    historical_weather = connect.execute("SELECT avg(humidity) as h FROM sqlpublic.dublin_weather Where DOW = 'Tuesday'")
    for i in historical_weather:
        dublin_weather.append(dict(i))
    historical_weather = connect.execute("SELECT avg(humidity) as h FROM sqlpublic.dublin_weather Where DOW = 'Wednesday'")
    for i in historical_weather:
        dublin_weather.append(dict(i))
    historical_weather = connect.execute("SELECT avg(humidity) as h FROM sqlpublic.dublin_weather Where DOW = 'Thursday'")
    for i in historical_weather:
        dublin_weather.append(dict(i))
    historical_weather = connect.execute("SELECT avg(humidity) as h FROM sqlpublic.dublin_weather Where DOW = 'Friday'")
    for i in historical_weather:
        dublin_weather.append(dict(i))
    historical_weather = connect.execute("SELECT avg(humidity) as h FROM sqlpublic.dublin_weather Where DOW = 'Saturday'")
    for i in historical_weather:
        dublin_weather.append(dict(i))
    historical_weather = connect.execute("SELECT avg(humidity) as h FROM sqlpublic.dublin_weather Where DOW = 'Sunday'")
    for i in historical_weather:
        dublin_weather.append(dict(i))
    
    jsonify(dublin_weather=dublin_weather)


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
    
    return render_template("index.html", data=points, weather=weather, averages=averages,dublin_weather=dublin_weather)
