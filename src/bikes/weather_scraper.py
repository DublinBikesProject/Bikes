
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
        
        add_weather = ("REPLACE INTO test "
                    "(id, main, desc, temp, icon, pressure, humidity, temp_min, temp_max, visibility, windspeed) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                       )

        
        cursor.execute(add_weather, data)
        
        db.commit()
        
        
    except Exception as e: 
        template = "Insert An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print(message)

def main(): 

    url = "http://api.openweathermap.org/data/2.5/weather?q=dublin,ie&units=metric&appid=a87a4c45fc8819c6fd6dae5a0db2439a"
    db = dbConnect()
    print("Connected!")
    while True: 
        rawData = requests.get(url)
        print(rawData.status_code)
        if rawData.status_code == 200:
            data = json.loads(rawData.text)
            print("Working")
            id = data['sys']['country']
            print(id)
            main = data['weather'][0]['main']
            desc = data['weather'][0]['description']
            temp = data['main']['temp']
            icon = data['weather'][0]['icon']
            pressure = data['main']['pressure']
            humidity = data['main']['humidity']
            temp_min = data['main']['temp_min']
            temp_max = data['main']['temp_max']
            visibility = data['visibility']                           
            
            data = [id, main, desc, temp, icon, pressure, humidity, temp_min, temp_max, visibility]
            insertDb(data, db)
        time.sleep(1800)
           
if __name__ == "__main__":
    main()
