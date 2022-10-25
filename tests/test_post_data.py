import os
import random
import json
import unittest
import requests
from dotenv import load_dotenv
load_dotenv()
from login_utils import get_access_token, query_get, query_post,data


class MyTestCase(unittest.TestCase):
  url="http://127.0.0.1:8000/api/post_data"

  signincred = {
    "AADHAR_NO": f"{os.environ['ADMIN_ID']}",
    "password": f"{os.environ['ADMIN_PWD']}",
    "village_name": f"{os.environ['ADMIN_VILLAGE_NAME']}",
    "role": f"{os.environ['ADMIN_role']}"
  }


  def test_post2db_existing(self):
    headers={
    "accept":"application/json",
    "Authorization":f"Bearer {get_access_token(MyTestCase.signincred)}",
    "Content-Type":"application/json"
    }
    dumpdata=json.dumps(data)
    response = requests.post(MyTestCase.url, data=dumpdata,headers=headers)
    print(response.json())
    self.assertEqual(response.json()['status'], 'abort')  # add assertion here

  def test_post2db_new(self):
    newdata=data
    newdata["respondent_prof"]["id_no"]=str(random.randint(1,1000000000000000))

    headers={
    "accept":"application/json",
    "Authorization":f"Bearer {get_access_token(MyTestCase.signincred)}",
    "Content-Type":"application/json"
    }
    dumpdata=json.dumps(newdata)
    response = requests.post(MyTestCase.url, data=dumpdata,headers=headers)
    self.assertEqual(response.json()['status'], 'success')  # add assertion here

  def test_unauthenticated(self):
    headers={
      "accept":"application/json",
      "Content-Type":"application/json"}
    dumpdata=json.dumps(data) 
    response = requests.post(MyTestCase.url, data=dumpdata,headers=headers)
    print(response.status_code)
    self.assertEqual(response.status_code, 403)  # add assertion here



if __name__ == '__main__':
    unittest.main()
