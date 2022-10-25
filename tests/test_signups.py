import os
import random
import json
import unittest
import requests
from dotenv import load_dotenv
load_dotenv()
from login_utils import get_access_token

  #only admin can signup new users  
class MySignupTestCase(unittest.TestCase):
    url="http://127.0.0.1:8000/signup"
    signincred = {
        "AADHAR_NO": f"{os.environ['ADMIN_ID']}",
        "password": f"{os.environ['ADMIN_PWD']}",
        "village_name": f"{os.environ['ADMIN_VILLAGE_NAME']}",
        "role": f"{os.environ['ADMIN_role']}"
        }
    
    def test_signup_owner_existing_account(self):
        MySignupTestCase.signincred["role"]=os.environ['OWNER_role']
        headers={
        "accept":"application/json",
        "Authorization":f"Bearer {get_access_token(MySignupTestCase.signincred)}",
        "Content-Type":"application/json"
        }
        signupcredexist={
        "AADHAR_NO": f"{os.environ['ADMIN_ID']}",
        "password": f"{os.environ['ADMIN_PWD']}",
        "village_name": f"{os.environ['ADMIN_VILLAGE_NAME']}",
        "role": f"{os.environ['USER_role']}"
        }
        signupcredexistowner=json.dumps(signupcredexist)
        response=requests.post(MySignupTestCase.url,headers=headers,data=signupcredexistowner)
        self.assertEqual(response.json()['status'], 'failed')

    def test_signup_owner_new_account(self):
        MySignupTestCase.signincred["role"]=os.environ['OWNER_role']
        headers={
        "accept":"application/json",
        "Authorization":f"Bearer {get_access_token(MySignupTestCase.signincred)}",
        "Content-Type":"application/json"
        }
        signupcrednewowner={
        "AADHAR_NO": random.randint(1,1000000000000000),
        "password": f"{os.environ['ADMIN_PWD']}",
        "village_name": f"{os.environ['ADMIN_VILLAGE_NAME']}",
        "role": f"{os.environ['USER_role']}"
        }
        signupcredowner=json.dumps(signupcrednewowner)
        response=requests.post(MySignupTestCase.url,headers=headers,data=signupcredowner)
        self.assertEqual(response.json()['status'], 'success')    

    def test_signup_admin(self):
        MySignupTestCase.signincred["role"]=os.environ['ADMIN_role']
        headers={
        "accept":"application/json",
        "Authorization":f"Bearer {get_access_token(MySignupTestCase.signincred)}",
        "Content-Type":"application/json"
        }
        signupcredadmin={
        "AADHAR_NO": random.randint(1,1000000000000000),
        "password": f"{os.environ['ADMIN_PWD']}",
        "village_name": f"{os.environ['ADMIN_VILLAGE_NAME']}",
        "role": f"{os.environ['ADMIN_role']}"
        }
        signupcredadmin=json.dumps(signupcredadmin)
        response=requests.post(MySignupTestCase.url,headers=headers,data=signupcredadmin)
        self.assertEqual(response.json()['status'], 'success') 

    def test_signup_user(self):
        MySignupTestCase.signincred["role"]=os.environ['USER_role']
        headers={
        "accept":"application/json",
        "Authorization":f"Bearer {get_access_token(MySignupTestCase.signincred)}",
        "Content-Type":"application/json"
        }
        signupcreduser={
        "AADHAR_NO": f"{os.environ['ADMIN_ID']}",
        "password": f"{os.environ['ADMIN_PWD']}",
        "village_name": f"{os.environ['ADMIN_VILLAGE_NAME']}",
        "role": f"{os.environ['OWNER_role']}"
        }
        signupcreduser=json.dumps(signupcreduser)
        response=requests.post(MySignupTestCase.url,headers=headers,data=signupcreduser)
        self.assertEqual(response.json()['status'], 'not_allowed')

    def test_unauth(self):  
        signupcred={
        "AADHAR_NO": f"{os.environ['ADMIN_ID']}",
        "password": f"{os.environ['ADMIN_PWD']}",
        "village_name": f"{os.environ['ADMIN_VILLAGE_NAME']}",
        "role": f"{os.environ['OWNER_role']}"
        }
        signupcred=json.dumps(signupcred)
        response=requests.post(MySignupTestCase.url,data=signupcred)
        self.assertEqual(response.status_code, 403)


if __name__=="__main__":
    unittest.main()