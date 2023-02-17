import os
import unittest
import requests
import json
from login_utils import get_access_token, BASE_URL


class TestFetchFamilyData(unittest.TestCase):
    url = BASE_URL + "/api/get_familydata"

    params = {"respondents_id": "test"}

    signincred = {
        "AADHAR_NO": f"{os.environ['ADMIN_ID']}",
        "password": f"{os.environ['ADMIN_PWD']}",
        "village_name": f"{os.environ['ADMIN_VILLAGE_NAME']}",
        "role": f"{os.environ['OWNER_ROLE']}"
        }

    def test_owner(self):
        
        TestFetchFamilyData.signincred['role'] = os.environ['OWNER_ROLE']

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {get_access_token(TestFetchFamilyData.signincred)}",
            "Content-Type": "application/json"
        }
        response = requests.get(url=TestFetchFamilyData.url, params=TestFetchFamilyData.params, headers=headers)
        self.assertEqual(response.status_code, 401)

    def test_admin(self):
        TestFetchFamilyData.signincred['role'] = os.environ['ADMIN_ROLE']

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {get_access_token(TestFetchFamilyData.signincred)}",
            "Content-Type": "application/json"
        }
        response = requests.get(url=TestFetchFamilyData.url, params=TestFetchFamilyData.params, headers=headers)
        with open('intended_responses/fetch_fam_data.json', 'r') as f:
            data = json.load(f)
            self.assertEqual(response.json(), data)

    def test_user(self):
        TestFetchFamilyData.signincred['role'] = os.environ['USER_ROLE']

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {get_access_token(TestFetchFamilyData.signincred)}",
            "Content-Type": "application/json"
        }
        response = requests.get(url=TestFetchFamilyData.url, params=TestFetchFamilyData.params, headers=headers)
        self.assertEqual(response.status_code, 401)

    def test_unauth(self):
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        response = requests.get(url=TestFetchFamilyData.url, params=TestFetchFamilyData.params, headers=headers)
        self.assertEqual(response.json()['detail'], "Not authenticated")



if __name__ == '__main__':
    unittest.main()
