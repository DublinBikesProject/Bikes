import pymysql
import json
import requests
import pandas as pd
from pymysql.err import IntegrityError
from time import sleep, strftime, gmtime
from bs4 import BeautifulSoup
import pymysql.cursors
import datetime
    
def dbconnect():
    """ Function to establish connection to the database """
    
    try:
        db = pymysql.connect(
            host='34.209.36.30', # database IP
            user='sqlpublic',
            passwd='sqlpublic',
            db='publicdb'
        )
        
    except Exception as e: # error handling
        sys.exit("Can't connect to database")
    return db

def insertDb(data, db):
    """ Function to write to the database """

    try:
        cursor = db.cursor()
        add_bike = ("INSERT INTO bikes "
                    "(address, available_bike_stands, available_bikes, last_update, lat, lng, status) "
                    "VALUES (%(address)s, %(available_bike_stands)s, %(available_bikes)s, %(last_update)s, %(lat)s, %(lng)s), %(status)s")

        cursor.execute(add_bike, data)
        db.commit()#write

    except Exception as ex: # error handling
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)

def main():
    url = 'https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=163a27dc14a77d825fb26c4212d74477642b4469' # the website containing the data
    db = dbconnect() # invoke the connect function AKA create the connection to the database
    print("Connected")
    while True: #infinite loop
        web_data = requests.get(url)
        print(web_data.status_code)
        if web_data.status_code == 200:
            data = json.loads(web_data.text)
            
            for i in range(100): # there are 100 stations with index 0-99)
                data[i]['lat'] = data[i]['position']['lat']
                data[i]['lng'] = data[i]['position']['lng']
                data[i]['last_update'] = datetime.datetime.fromtimestamp(int(data[i]['last_update']/1000)).strftime('%Y-%m-%d %H:%M:%S')
                insertDb(data[i], db)# invoke the write to database function
            
        print("sleeping for 5 minutes")
        sleep(300) # 5 minute break and scrape again
    
if __name__ == '__main__':
    main()
    




