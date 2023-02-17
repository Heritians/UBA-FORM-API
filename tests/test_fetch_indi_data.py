import os
import unittest
import requests
import json
from login_utils import get_access_token, BASE_URL


class TestFetchIndividualData(unittest.TestCase):
    url = BASE_URL + "/api/get_individual_data"

    signincred = {
        "AADHAR_NO": f"{os.environ['ADMIN_ID']}",
        "password": f"{os.environ['ADMIN_PWD']}",
        "village_name": f"{os.environ['ADMIN_VILLAGE_NAME']}",
        "role": f"{os.environ['OWNER_ROLE']}"
        }

    params = {"respondents_id": "test_sub"}

    def test_owner(self):
        
        TestFetchIndividualData.signincred['role'] = os.environ['OWNER_ROLE']
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {get_access_token(TestFetchIndividualData.signincred)}",
            "Content-Type": "application/json"
        }
        response = requests.get(url=TestFetchIndividualData.url, params=TestFetchIndividualData.params, headers=headers)
        self.assertEqual(response.status_code, 401)

    def test_admin(self):
        TestFetchIndividualData.signincred['role'] = os.environ['ADMIN_ROLE']
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {get_access_token(TestFetchIndividualData.signincred)}",
            "Content-Type": "application/json"
        }
        response = requests.get(url=TestFetchIndividualData.url, params=TestFetchIndividualData.params, headers=headers)
        with open("tests/intended_responses/fetch_indiv_data.json", 'r') as f:
            data = json.load(f)
            self.assertEqual(response.json(), data)

    def test_user(self):
        TestFetchIndividualData.signincred['role'] = os.environ['USER_ROLE']
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {get_access_token(TestFetchIndividualData.signincred)}",
            "Content-Type": "application/json"
        }
        response = requests.get(url=TestFetchIndividualData.url, params=TestFetchIndividualData.params, headers=headers)
        self.assertEqual(response.status_code, 401)

    def test_unauth(self):
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        response = requests.get(url=TestFetchIndividualData.url, params=TestFetchIndividualData.params, headers=headers)
        self.assertEqual(response.json()['detail'], "Not authenticated")


if __name__ == '__main__':
    unittest.main()
