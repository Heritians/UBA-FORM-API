import unittest
import os
import unittest
import requests
from dotenv import load_dotenv

load_dotenv()
from login_utils import get_access_token


class TestFetchIndividualData(unittest.TestCase):
    url = "http://127.0.0.1:8000/api/get_familydata"

    def test_owner(self):
        signincred = {
            "AADHAR_NO": f"{os.environ['ADMIN_ID']}",
            "password": f"{os.environ['ADMIN_PWD']}",
            "village_name": f"{os.environ['ADMIN_VILLAGE_NAME']}",
            "role": f"{os.environ['OWNER_ROLE']}"
        }
        params = {"respondents_id": "8523705708935799"}
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {get_access_token(signincred)}",
            "Content-Type": "application/json"
        }
        response = requests.get(url=TestFetchIndividualData.url, params=params, headers=headers)
        self.assertEqual(response.json()['message'], ['Wrong endpoint'])

    def test_admin(self):
        signincred = {
            "AADHAR_NO": f"{os.environ['ADMIN_ID']}",
            "password": f"{os.environ['ADMIN_PWD']}",
            "village_name": f"{os.environ['ADMIN_VILLAGE_NAME']}",
            "role": f"{os.environ['ADMIN_ROLE']}"
        }
        params = {"respondents_id": "8523705708935799"}
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {get_access_token(signincred)}",
            "Content-Type": "application/json"
        }
        response = requests.get(url=TestFetchIndividualData.url, params=params, headers=headers)
        self.assertEqual(response.json()['status'], "success")

    def test_user(self):
        signincred = {
            "AADHAR_NO": f"{os.environ['ADMIN_ID']}",
            "password": f"{os.environ['ADMIN_PWD']}",
            "village_name": f"{os.environ['ADMIN_VILLAGE_NAME']}",
            "role": f"{os.environ['USER_ROLE']}"
        }
        params = {"respondents_id": "8523705708935799"}
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {get_access_token(signincred)}",
            "Content-Type": "application/json"
        }
        response = requests.get(url=TestFetchIndividualData.url, params=params, headers=headers)
        self.assertEqual(response.json()['message'], ["Not authorized"])


if __name__ == '__main__':
    unittest.main()
