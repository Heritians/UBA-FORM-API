import os
import json
import unittest
import requests
from login_utils import get_access_token, BASE_URL

class MyDeleteDatabaseTest(unittest.TestCase):
    
    signincred = {
        "AADHAR_NO": f"{os.environ['ADMIN_ID']}",
        "password": f"{os.environ['ADMIN_PWD']}",
        "village_name": f"{os.environ['ADMIN_VILLAGE_NAME']}",
        "role": f"{os.environ['ADMIN_ROLE']}"
        }

    params={"dbname":"test_db"}
    DEL_VILLAGE_NAME=BASE_URL+"/ops/delete_database"
    GET_VILLAGE_LIST=BASE_URL+"/ops/get_village_list"
    PUT_URL=BASE_URL+'/ops/update_village_list'

    def test_delete_database_user(self):
        MyDeleteDatabaseTest.signincred["role"]=os.environ["USER_ROLE"]
        headers={
            "accept":"application/json",
            "Authorization":f"Bearer {get_access_token(MyDeleteDatabaseTest.signincred)}",
        }
        response=requests.delete(MyDeleteDatabaseTest.DEL_VILLAGE_NAME,headers=headers,params=MyDeleteDatabaseTest.params)
        self.assertEqual(response.status_code, 401)

    def test_delete_database_admin(self):
        MyDeleteDatabaseTest.signincred["role"]=os.environ["ADMIN_ROLE"]
        headers={
            "accept":"application/json",
            "Authorization":f"Bearer {get_access_token(MyDeleteDatabaseTest.signincred)}",
        }
        response=requests.delete(MyDeleteDatabaseTest.DEL_VILLAGE_NAME,headers=headers,params=MyDeleteDatabaseTest.params)
        self.assertEqual(response.status_code, 401)    
        
    def test_delete_existing_database_owner(self):
        MyDeleteDatabaseTest.signincred["role"]=os.environ["OWNER_ROLE"]
        headers={
            "accept":"application/json",
            "Authorization":f"Bearer {get_access_token(MyDeleteDatabaseTest.signincred)}",
        }
        response=None
        get_response=requests.get(MyDeleteDatabaseTest.GET_VILLAGE_LIST,headers=headers)
        if MyDeleteDatabaseTest.params["dbname"] in get_response.json()["data"]["village_names"]:
            response=requests.delete(MyDeleteDatabaseTest.DEL_VILLAGE_NAME,headers=headers,params=MyDeleteDatabaseTest.params)
        else:
            response=requests.put(MyDeleteDatabaseTest.PUT_URL,headers=headers,params=MyDeleteDatabaseTest.params)
            response=requests.delete(MyDeleteDatabaseTest.DEL_VILLAGE_NAME,headers=headers,params=MyDeleteDatabaseTest.params)
        self.assertEqual(response.status_code, 200) 

    def test_delete_nonexisting_database_owner(self):
        MyDeleteDatabaseTest.signincred["role"]=os.environ["OWNER_ROLE"]
        headers={
            "accept":"application/json",
            "Authorization":f"Bearer {get_access_token(MyDeleteDatabaseTest.signincred)}",
        }
        response=None
        get_response=requests.get(MyDeleteDatabaseTest.GET_VILLAGE_LIST,headers=headers)
        if MyDeleteDatabaseTest.params["dbname"] in get_response.json()["data"]["village_names"]:
            response=requests.delete(MyDeleteDatabaseTest.DEL_VILLAGE_NAME,headers=headers,params=MyDeleteDatabaseTest.params)
            response=requests.delete(MyDeleteDatabaseTest.DEL_VILLAGE_NAME,headers=headers,params=MyDeleteDatabaseTest.params)
        else:
            response=requests.delete(MyDeleteDatabaseTest.DEL_VILLAGE_NAME,headers=headers,params=MyDeleteDatabaseTest.params)
        self.assertEqual(response.status_code, 400) 

    def test_unauth(self):
        headers={
            "accept":"application/json"
        }
        response=requests.delete(MyDeleteDatabaseTest.DEL_VILLAGE_NAME,headers=headers,params=MyDeleteDatabaseTest.params)
        return self.assertEqual(response.status_code,403)       
        

if __name__ == "__main__":
    unittest.main()
