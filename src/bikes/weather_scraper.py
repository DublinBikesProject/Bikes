
import requests
import json
import time 
import pymysql
import pandas as pd
from pymysql.err import IntegrityError
from time import sleep, strftime, gmtime
import pymysql.cursors
import datetime
import sys

def dbConnect():
    try:
        db = pymysql.connect(
            host='52.43.48.163',
            user='publicdb',
            passwd='sqlpublic',
            db='sqlpublic'
        )
        
    except Exception as e: 
        sys.exit("Cannot connect to database")
    return db
    
def insertDb(data, db):
    
    try:
        cursor = db.cursor()
        
        add_weather = ("REPLACE INTO weather "
                    "(id, main, description, temp, icon, pressure, humidity, temp_min, temp_max, windspeed, threeH_rain_predict, future_icon ) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        
        cursor.execute(add_weather, data)
        db.commit()
        
    except Exception as e: 
        template = "Insert An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print(message)

def main(): 

    url = "http://api.openweathermap.org/data/2.5/forecast?q=dublin,ie&units=metric&appid=a87a4c45fc8819c6fd6dae5a0db2439a"
    db = dbConnect()
    print("Connected!")
    while True: 
        rawData = requests.get(url)
        print(rawData.status_code)

        if rawData.status_code == 200:
            data = json.loads(rawData.text)
            print("Working")
            id = data['city']['country']
            print(id)

            main = data['list'][0]['weather'][0]['main']
            desc = data['list'][0]['weather'][0]['description']
            temp = data['list'][0]['main']['temp']
            icon = data['list'][0]['weather'][0]['icon']
            pressure = data['list'][0]['main']['pressure']
            humidity = data['list'][0]['main']['humidity']
            temp_min = data['list'][0]['main']['temp_min']
            temp_max = data['list'][0]['main']['temp_max']
            windspeed = data['list'][0]['wind']['speed']
            threeH_rain_predict = data['list'][1]['rain']['3h']
            future_icon = data['list'][1]['weather'][0]['icon']
            
            data = [id, main, desc, temp, icon, pressure, humidity, temp_min, temp_max, windspeed, threeH_rain_predict, future_icon]
            insertDb(data, db)

        
        print('sleeping') 
        time.sleep(1800)
           
if __name__ == "__main__":
    main()
