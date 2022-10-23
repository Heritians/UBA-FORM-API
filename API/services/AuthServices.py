import re
from API.utils.Auth import Auth
from ..models.AuthSchema import UserOut, UserAuth
from ..models.RequestBodySchema import FormData
from ..utils.DBQueries import DBQueries
from ..utils.DBConnection import DBConnection

from fastapi import status, HTTPException
from fastapi.responses import RedirectResponse


def signup(response_result,data:UserAuth):
    # querying database to check if user already exist
    user = DBQueries.filtered_db_search("Auth",data.role,[],AADHAR=data.AADHAR_NO)
    if len(list(user))!=0:
        response_result['status'] = f'failed'
        response_result['message'].append(f'User with this AADHAR NO already exist')
    else:    
        userinfo = {
            'AADHAR': data.AADHAR_NO,
            'password': Auth.get_password_hash(data.password),
            'village_name': data.village_name,
        }
        DBQueries.insert_to_database("Auth",data.role,userinfo)    # saving user to database
        response_result['status'] = f'success'
        response_result['message'].append(f'User with this AADHAR NO created successfully')