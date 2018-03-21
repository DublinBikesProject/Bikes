"""db = pymysql.connect(
            host='34.209.36.30', # database IP
            user='sqlpublic',
            passwd='sqlpublic',
            db='publicdb'
        )"""


def db_connect(query):
    import MySQLdb
    db = MySQLdb.connect("34.209.36.30", "sqlpublic", "sqlpublic", "publicdb") 
    curs=db.cursor() 
    curs.execute(query)
    reading = curs.fetchall() 
    return reading

query = "SELECT lng FROM bikes WHERE address = 'Grand Canal Dock';"
print(db_connect(query))


