import pandas as pd
import csv

def db_connect(query):
    import MySQLdb
    db = MySQLdb.connect("34.209.36.30", "sqlpublic", "sqlpublic", "publicdb") 
    curs=db.cursor() 
    curs.execute(query)
    reading = curs.fetchall()
    return reading

example_query = "SELECT lng FROM bikes WHERE address = 'Grand Canal Dock';"

address = "SELECT distinct address,lat,lng FROM bikes;"
print(type(db_connect(address)))

for i in db_connect(address):
    name = i[0]
    lat = i[1]
    lng = i[2]
    locations =[name,lat, lng]
    with open('locations.csv',"a") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerow(locations)    

    
