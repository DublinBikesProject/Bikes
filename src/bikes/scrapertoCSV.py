# Adapted from the following source https://www.shanelynn.ie/scraping-dublin-city-bikes-data-using-python/
#
# City Bikes Scraper.

import requests
import pandas as pd
import pandas.io.sql as pdsql
from time import sleep, strftime, gmtime
import json
import sqlite3

SQLITE = False                      # If true - data is stored in SQLite file, if false - csv.
SQLITE_FILE = "bikedb.db"           # SQLite file to save data in
CSV_FILE = "output.csv"             # CSV file to save data in

def StationDetails():
    print("Scraping at", strftime("%Y%m%d%H%M%S", gmtime()))
    try:
        r = "https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=163a27dc14a77d825fb26c4212d74477642b4469"
        json_data = requests.get(r, proxies='')
        station_data = json.loads(json_data.content)
    
    except: 
        print ("~~~~~FAIL~~~~~")
        return None
    
    print ("~~~~~SUCCESS~~~~~")
    return station_data

def writeToCsv(data, filename="output.csv"):
    """
    Take the list of results and write as csv to filename.
    """
    data_frame = pd.DataFrame(data)
    data_frame['time'] = strftime("%Y%m%d%H%M%S", gmtime())
    data_frame.to_csv(filename, header=False, mode="a")


if __name__ == "__main__":
    
    while True:
        station_data = StationDetails()
        if station_data:
            if SQLITE:
                writeToDb(station_data, conn)
            else:  
                writeToCsv(station_data, filename="output.csv" )

        print("Sleeping for 300 seconds.")
        sleep(300)
        print()
