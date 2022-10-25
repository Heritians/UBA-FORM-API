import random
import json
import unittest
import requests
from dotenv import load_env
load_env()
from login_utils import get_access_token, query_get, query_post,data


class MyTestCase(unittest.TestCase):
  url="http://127.0.0.1:8000/api/post_data"


  def test_post2db_existing(self):
    signincred={
    "AADHAR_NO": "string",
    "password": "string",
    "village_name": "string",
    "role": "string"
    } 
    headers={
    "accept":"application/json",
    "Authorization":f"Bearer {get_access_token(signincred)}",
    "Content-Type":"application/json"
    }
    dumpdata=json.dumps(data)
    response = requests.post(MyTestCase.url, data=dumpdata,headers=headers)
    self.assertEqual(response.json()['status'], 'abort')  # add assertion here

  def test_post2db_new(self):
    newdata=data
    newdata["respondent_prof"]["id_no"]=str(random.randint(1,1000000000000000))
    signincred={
    "AADHAR_NO": "5734219582373335",
    "password": "string",
    "village_name": "Sehore",
    "role": "admin"
    } 
    headers={
    "accept":"application/json",
    "Authorization":f"Bearer {get_access_token(signincred)}",
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



if __name__ == '__main__':
    unittest.main()
