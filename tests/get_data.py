import unittest
from API.services.DBManipulation import fetch_from_db



class MyGetTestCase(unittest.TestCase):
    def get_something(self):
        import requests

        url = "http://localhost:8000/api/get_data"
        retreive=requests.get(url)
        print(retreive.text)
        self.assertEqual(retreive.text,"200")

if __name__=="__main__":
    unittest.main()        