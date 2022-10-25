import os
import unittest
import requests
from login_utils import get_access_token, BASE_URL



class MyGetTestCase(unittest.TestCase):
    url = BASE_URL + "/api/get_data"

    def test_get_fromdb_owner(self):
        signincred = {
            "AADHAR_NO": f"{os.environ['ADMIN_ID']}",
            "password": f"{os.environ['ADMIN_PWD']}",
            "village_name": f"{os.environ['ADMIN_VILLAGE_NAME']}",
            "role": f"{os.environ['OWNER_role']}"
        }
        params = {"village_name": "Sehore"}
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {get_access_token(signincred)}",
            "Content-Type": "application/json",
        }
        response=requests.get(url=MyGetTestCase.url, params=params, headers=headers)
        self.assertEqual(response.json()['status'], "success")


    def test_get_fromdb_admin(self):
        signincred = {
            "AADHAR_NO": f"{os.environ['ADMIN_ID']}",
            "password": f"{os.environ['ADMIN_PWD']}",
            "village_name": f"{os.environ['ADMIN_VILLAGE_NAME']}",
            "role": f"{os.environ['ADMIN_role']}"
        }
        params = {"village_name": "None"}
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {get_access_token(signincred)}",
            "Content-Type": "application/json",
        }
        response=requests.get(url=MyGetTestCase.url, params=params, headers=headers)
        self.assertEqual(response.json()['status'], "success")

    def test_get_fromdb_user(self):
        signincred = {
            "AADHAR_NO": f"{os.environ['ADMIN_ID']}",
            "password": f"{os.environ['ADMIN_PWD']}",
            "village_name": f"{os.environ['ADMIN_VILLAGE_NAME']}",
            "role": f"{os.environ['USER_role']}"
        }
        params = {"village_name": "None"}
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {get_access_token(signincred)}",
            "Content-Type": "application/json",
        }
        response=requests.get(url=MyGetTestCase.url, params=params, headers=headers)
        self.assertEqual(response.json()['status'], "not_allowed")

if __name__=="__main__":
    unittest.main()        
