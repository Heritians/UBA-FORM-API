import os
import json
import requests
import unittest
from login_utils import get_access_token, BASE_URL

class MyUpdateVillageListTest(unittest.TestCase):
    signincred = {
        "AADHAR_NO": f"{os.environ['ADMIN_ID']}",
        "password": f"{os.environ['ADMIN_PWD']}",
        "village_name": f"{os.environ['ADMIN_VILLAGE_NAME']}",
        "role": f"{os.environ['ADMIN_ROLE']}"
        }
    
    params={"dbname":"db_test"}

    GET_VILLAGE_LIST=BASE_URL+"/api/get_village_list"
    DEL_VILLAGE_NAME=BASE_URL+"/ops/delete_database"
    PUT_URL=BASE_URL+'/ops/update_village_list'
    
    def test_update_village_user(self):
        MyUpdateVillageListTest.signincred["role"]=os.environ["USER_ROLE"]
        headers={
            "accept":"application/json",
            "Authorization":f"Bearer {get_access_token(MyUpdateVillageListTest.signincred)}"
        }
        response=requests.put(MyUpdateVillageListTest.PUT_URL,headers=headers,params=MyUpdateVillageListTest.params)
        return self.assertEqual(response.status_code,401)
    
    def test_update_village_admin(self):
        MyUpdateVillageListTest.signincred["role"]=os.environ["ADMIN_ROLE"]
        headers={
            "accept":"application/json",
            "Authorization":f"Bearer {get_access_token(MyUpdateVillageListTest.signincred)}"
        }
        response=requests.put(MyUpdateVillageListTest.PUT_URL,headers=headers,params=MyUpdateVillageListTest.params)
        return self.assertEqual(response.status_code,401)
    
    def test_update_existing_village_owner(self):
        MyUpdateVillageListTest.signincred["role"]=os.environ["OWNER_ROLE"]

        headers={
            "accept":"application/json",
            "Authorization":f"Bearer {get_access_token(MyUpdateVillageListTest.signincred)}"
        }
        get_response=requests.get(MyUpdateVillageListTest.GET_VILLAGE_LIST,headers=headers)
        if MyUpdateVillageListTest.params["dbname"] in get_response.json()["data"]["village_names"]:
            response=requests.put(MyUpdateVillageListTest.PUT_URL,headers=headers,params=MyUpdateVillageListTest.params)
            
        else:
            response=requests.put(MyUpdateVillageListTest.PUT_URL,headers=headers,params=MyUpdateVillageListTest.params)
            response=requests.put(MyUpdateVillageListTest.PUT_URL,headers=headers,params=MyUpdateVillageListTest.params)
        
        requests.put(MyUpdateVillageListTest.DEL_VILLAGE_NAME,headers=headers,params=MyUpdateVillageListTest.params)
        return self.assertEqual(response.status_code,409)
        
    def test_update_new_village_owner(self):
        
        MyUpdateVillageListTest.signincred["role"]=os.environ["OWNER_ROLE"]
        response=None

        headers={
            "accept":"application/json",
            "Authorization":f"Bearer {get_access_token(MyUpdateVillageListTest.signincred)}"
        }
        get_response=requests.get(MyUpdateVillageListTest.GET_VILLAGE_LIST,headers=headers)
        if MyUpdateVillageListTest.params["dbname"] in get_response.json()["data"]["village_names"]:
            del_response=requests.delete(MyUpdateVillageListTest.DEL_VILLAGE_NAME,headers=headers,params=MyUpdateVillageListTest.params)
            response=requests.put(MyUpdateVillageListTest.PUT_URL,headers=headers,params=MyUpdateVillageListTest.params)
        else:
            response=requests.put(MyUpdateVillageListTest.PUT_URL,headers=headers,params=MyUpdateVillageListTest.params)
        
        requests.put(MyUpdateVillageListTest.DEL_VILLAGE_NAME,headers=headers,params=MyUpdateVillageListTest.params)
        return self.assertEqual(response.status_code,200)
    
    def test_unauth(self):
        headers={
            "accept":"application/json"
        }
        response=requests.put(MyUpdateVillageListTest.PUT_URL,headers=headers,params=MyUpdateVillageListTest.params)
        return self.assertEqual(response.status_code,403)
    

if __name__=="__main__":
    unittest.main()    

