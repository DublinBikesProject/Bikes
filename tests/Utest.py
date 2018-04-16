import unittest


from Bikes.src.bikes.weather_scraper import *

class TestSetAdt(unittest.TestCase):
    
    def test_connection(self):
        
        self.assertTrue(rawData.status_code==200)

    def test_city(self):
        city = data['city']['name']
        self.assertTrue(city == "Dublin")
        
    
      
        
        
        
if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestSetAdt)
    unittest.TextTestRunner().run(suite)
        
