import unittest
from sqlalchemy import create_engine
import pymysql

from weather_scraper import *

class TestSetAdt(unittest.TestCase):
    
    def test_connection_weather_API(self):
        #checks if the weather API connection works"
        url = "http://api.openweathermap.org/data/2.5/forecast?q=dublin,ie&units=metric&appid=a87a4c45fc8819c6fd6dae5a0db2439a"
        rawData = requests.get(url)
        self.assertTrue(rawData.status_code==200)

    def test_city(self):
        #checks for city name of API data
        url = "http://api.openweathermap.org/data/2.5/forecast?q=dublin,ie&units=metric&appid=a87a4c45fc8819c6fd6dae5a0db2439a"
        rawData = requests.get(url)
        data = json.loads(rawData.text)
        city = data['city']['name']
        self.assertTrue(city == "Dublin")

    def test_connection_JCDecaux_API(self):
        #checks if the JCDecaux API connection works"
        url = 'https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=163a27dc14a77d825fb26c4212d74477642b4469' # the website containing the data
        web_data = requests.get(url)
        self.assertTrue(web_data.status_code==200)        

    def test_query(self):
        # testing query returns correct output and DB connection
        stations = []
        engine = create_engine("mysql+pymysql://publicdb:sqlpublic@52.43.48.163:3306/sqlpublic",echo=False)
        connection = engine.connect()
        trans = connection.begin()
        rows = connection.execute("Select distinct(lat),lng from bikes where address = 'Bolton Street'")
        trans.commit()
        for i in rows:
            stations.append(dict(i))
        self.assertTrue(stations==[{'lat': 53.3512, 'lng': -6.269859}])

    def test_query_2(self):
        # testing query returns correct output and DB connection
        weather_id = []
        engine = create_engine("mysql+pymysql://publicdb:sqlpublic@52.43.48.163:3306/sqlpublic",echo=False)
        connection = engine.connect()
        trans = connection.begin()
        rows = connection.execute("SELECT id FROM weather")
        trans.commit()
        for i in rows:
            weather_id.append(dict(i))
        self.assertTrue(weather_id==[{'id': "IE"}])

    def test_query3(self):
        # testing query returns correct output and DB connection
        stations = []
        engine = create_engine("mysql+pymysql://publicdb:sqlpublic@52.43.48.163:3306/sqlpublic",echo=False)
        connection = engine.connect()
        trans = connection.begin()
        rows = connection.execute("Select distinct(lat),lng from bikes where address = 'George''s Lane'") # Query only works if the apostrophe is doubled up. 
        trans.commit()
        for i in rows:
            stations.append(dict(i))
        print(stations)
        self.assertTrue(stations==[{'lat': 53.3502, 'lng': -6.279696}])
        
if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestSetAdt)
    unittest.TextTestRunner().run(suite)
        
