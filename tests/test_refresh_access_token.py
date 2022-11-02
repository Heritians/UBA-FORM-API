import os
import random
import json
import unittest
import requests
from login_utils import get_access_token, BASE_URL

class TestRefreshAccessToken(unittest.TestCase):
    url=BASE_URL+"/auth/use_refresh_token"
    signincred = {
    "AADHAR_NO": f"{os.environ['ADMIN_ID']}",
    "password": f"{os.environ['ADMIN_PWD']}",
    "village_name": f"{os.environ['ADMIN_VILLAGE_NAME']}",
    "role": f"{os.environ['ADMIN_ROLE']}"
    }

    def test_refresh_access_token(self):
        tokens=get_access_token(TestRefreshAccessToken.signincred,return_refresh_token=True)
        headers={
        "accept":"application/json",
        "Authorization":f"Bearer {tokens[0]}",
        "Content-Type":"application/json"
        }
        response = requests.post(TestRefreshAccessToken.url, headers=headers,data=json.dumps({"refresh_access_token":tokens[1]}))
        self.assertEqual(response.status_code, 200)

    def test_unauth(self):  
        response=requests.post(TestRefreshAccessToken.url,data=json.dumps({"refresh_access_token":"string"}))
        self.assertEqual(response.status_code, 403)    

if __name__=="__main__":
    unittest.main()        