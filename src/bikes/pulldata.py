def db_connect(query):
    import MySQLdb
    db = MySQLdb.connect("34.209.36.30", "sqlpublic", "sqlpublic", "publicdb") 
    curs=db.cursor() 
    curs.execute(query)
    reading = curs.fetchall()
    return reading

query = "SELECT lng FROM bikes WHERE address = 'Grand Canal Dock';"
#print(db_connect(query))

address = "SELECT distinct address,lat,lng FROM bikes;"
db_connect(address)

for i in db_connect(address):
    print("Station is",i[0],"Latitude is",i[1],"Longitude is",i[2])

