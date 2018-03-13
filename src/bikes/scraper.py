import pymysql
import json
import requests
import pandas as pd
from pandas.io.json import json_normalize
import pandas.io.sql as pdsql
from time import sleep, strftime, gmtime
import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pymysql.cursors

# function to establish connection to the database
def dbconnect():
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

# function to write to the database
def insertDb(data, db):
    try:
        db = dbconnect() # connect
        cursor = db.cursor()
    
        add_bike = ("INSERT INTO bikes "
                    "(bikes, name, idx, lat, timestamp, lng, id, free, number) "
                    "VALUES (%(bikes)s, %(name)s, %(idx)s, %(lat)s, %(timestamp)s, %(lng)s, %(id)s, %(free)s, %(number)s)")

        cursor.execute(add_bike, data)
        db.commit() #write
       
    except Exception as e: # error handling
        print (e)


url = 'http://api.citybik.es/dublinbikes.json' # the website containing the data
db = dbconnect() # invoke the connect function AKA create the connection to the database
while True: #infinite loop
    for i in range(100): # there are 100 stations with index 0-99
        data = json.loads(requests.get(
        url=url,
        params={'bikes': i,'name': i,'idx': i,'lat': i,'timestamp': i,'lng': i,'id': i,'free': i,'number': i}).text)[i]
        insertDb(data, db) # invoke the write to database function
    print("sleeping for 5 minutes")
    sleep(300) # 5 minute break and scrape again
    




