import os
import unittest
import requests
from login_utils import get_access_token, BASE_URL


class TestFetchIndividualData(unittest.TestCase):
    url = BASE_URL + "/api/get_individual_data"


    params = {"respondents_id": "305040848937547"}

    def test_owner(self):
        signincred = {
        "AADHAR_NO": f"{os.environ['ADMIN_ID']}",
        "password": f"{os.environ['ADMIN_PWD']}",
        "village_name": f"{os.environ['ADMIN_VILLAGE_NAME']}",
        "role": f"{os.environ['OWNER_ROLE']}"
        }
        signincred['role'] = os.environ['OWNER_ROLE']
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {get_access_token(signincred)}",
            "Content-Type": "application/json"
        }
        response = requests.get(url=TestFetchIndividualData.url, params=TestFetchIndividualData.params, headers=headers)
        self.assertEqual(response.json()['message'], ['Wrong endpoint'])

    def test_admin(self):
        signincred = {
        "AADHAR_NO": f"{os.environ['ADMIN_ID']}",
        "password": f"{os.environ['ADMIN_PWD']}",
        "village_name": f"{os.environ['ADMIN_VILLAGE_NAME']}",
        "role": f"{os.environ['OWNER_ROLE']}"
        }
        signincred['role'] = os.environ['ADMIN_ROLE']
        params = {"respondents_id": "2345"}
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
        "role": f"{os.environ['OWNER_ROLE']}"
        }
        signincred['role'] = os.environ['USER_ROLE']
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {get_access_token(signincred)}",
            "Content-Type": "application/json"
        }
        response = requests.get(url=TestFetchIndividualData.url, params=TestFetchIndividualData.params, headers=headers)
        self.assertEqual(response.json()['message'], ["Not authorized"])

    def test_unauth(self):
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        response = requests.get(url=TestFetchIndividualData.url, params=TestFetchIndividualData.params, headers=headers)
        self.assertEqual(response.json()['detail'], "Not authenticated")


if __name__ == '__main__':
    unittest.main()
