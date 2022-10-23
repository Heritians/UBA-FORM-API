import re
from API.utils.Auth import Auth
from ..models.AuthSchema import UserOut, UserAuth
from ..models.RequestBodySchema import FormData
from ..utils.DBQueries import DBQueries
from ..utils.DBConnection import DBConnection

from fastapi import status, HTTPException
from fastapi.responses import RedirectResponse


def signup(response_result, data: UserAuth):
    # querying database to check if user already exist
    user = DBQueries.filtered_db_search("Auth", data.role, [], AADHAR=data.AADHAR_NO)
    if len(list(user)) != 0:
        response_result['status'] = f'failed'
        response_result['message'].append(f'User with this AADHAR NO already exist')
    else:
        userinfo = {
            'AADHAR': data.AADHAR_NO,
            'password': Auth.get_password_hash(data.password),
            'village_name': data.village_name,
        }
        DBQueries.insert_to_database("Auth", data.role, userinfo)  # saving user to database
        response_result['status'] = f'success'
        response_result['message'].append(f'User with this AADHAR NO created successfully')


def user_login(tokens, form_data: UserAuth):
    user = DBQueries.filtered_db_search("Auth", form_data.role, ['_id'], AADHAR=form_data.AADHAR_NO)
    data = list(user)
    # print(list(user))
    print(data)
    if len(list(user)) == 0:
        tokens['status'] = 'Login failed'
    else:
        tokens['status'] = 'Login passed'

    # if not verify_password(form_data.password, hashed_pass):
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Incorrect email or password"
    #     )
    #
    # return {
    #     "access_token": create_access_token(user['email']),
    #     "refresh_token": create_refresh_token(user['email']),
    # }
