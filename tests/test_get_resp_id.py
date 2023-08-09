import os
import json
import unittest
import requests
from login_utils import get_access_token, BASE_URL

class MyGetRespIDTestCase(unittest.TestCase):
    url=BASE_URL+"/api/get_respid_list"

    with open("tests/intended_responses/respid_data.json","r") as f:
        data=json.load(f)

    def test_get_respid_owner_valid_village(self):
        signincred = {
            "AADHAR_NO": f"{os.environ['ADMIN_ID']}",
            "password": f"{os.environ['ADMIN_PWD']}",
            "village_name": f"{os.environ['ADMIN_VILLAGE_NAME']}",
            "role": f"{os.environ['OWNER_ROLE']}"
        }
        params={"date":"27-02-2023","village_name":"Sehore"}
        headers={
            "accept":"application/json",
            "Authorization": f"Bearer {get_access_token(signincred)}",
            "Content-Type": "application/json",
        }
        response=requests.get(url=self.url,params=params,headers=headers)
        self.assertEqual(response.json()["data"],self.data)

    def test_get_respid_owner_invalid_village(self):
        signincred = {
            "AADHAR_NO": f"{os.environ['ADMIN_ID']}",
            "password": f"{os.environ['ADMIN_PWD']}",
            "village_name": f"{os.environ['ADMIN_VILLAGE_NAME']}",
            "role": f"{os.environ['OWNER_ROLE']}"
        }
        params={"date":"27-02-2023","village_name":"villageDoesNotExist"}
        headers={
            "accept":"application/json",
            "Authorization": f"Bearer {get_access_token(signincred)}",
            "Content-Type": "application/json",
        }
        response=requests.get(url=self.url,params=params,headers=headers)
        self.assertEqual(response.status_code,400)

    def test_get_respid_admin(self):
        signincred = {
            "AADHAR_NO": f"{os.environ['ADMIN_ID']}",
            "password": f"{os.environ['ADMIN_PWD']}",
            "village_name": f"{os.environ['ADMIN_VILLAGE_NAME']}",
            "role": f"{os.environ['ADMIN_ROLE']}"
        }

        params={"date":"27-02-2023","village_name":"None"}   
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {get_access_token(signincred)}",
            "Content-Type": "application/json",
        }
        response=requests.get(url=self.url,params=params,headers=headers)
        self.assertEqual(response.json()["data"],self.data)

    def test_get_respid_user(self):
        signincred = {
            "AADHAR_NO": f"{os.environ['ADMIN_ID']}",
            "password": f"{os.environ['ADMIN_PWD']}",
            "village_name": f"{os.environ['ADMIN_VILLAGE_NAME']}",
            "role": f"{os.environ['USER_ROLE']}"
        }
        params={"date":"02-03-2023","village_name":"None"}
        headers={
            "accept":"application/json",
            "Authorization": f"Bearer {get_access_token(signincred)}",
            "Content-Type": "application/json",
        }
        response=requests.get(url=self.url,params=params,headers=headers)
        self.assertEqual(response.status_code,401)



if __name__=="__main__":
    unittest.main()        