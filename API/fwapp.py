from API import app
from API.utils.DBConnection import DBConnection
from .RequestBodySchema import FormData
from .ResponseBodySchema import EDAResponseData

from API.services.DBManipulation import *

import json


@app.get("/api/response_check")
def api_response_check():
    response_result = {
        'status': 'not_allowed',
        'message': ['Not authenticated'],
        'data': {}}
    try:
        db_msg = ""
        if DBConnection.flag:
            db_msg = "Connection Successful to db!"
        else:
            db_msg = "Connection failed to db"

        response_result['message'].append(db_msg)

    except Exception as e:
        print("Exception :", e)

    return response_result


@app.post("/api/post_data")
def api_post_data(responses: FormData):
    response_result = {
        'status': 'not_allowed',
        'message': ['Not authenticated'],
        'data': {}}
    try:
        commit_to_db(response_result, responses)
        return 200
    except Exception as e:
        print("Exception :", e)
        return 422

@app.get("/api/get_data")
def api_get_data(village_name:str):
    response_result = {
        'status': 'not_allowed',
        'message': ['Not authenticated'],
        'data': {}}
    try:
        response_data=fetch_from_db(response_result,village_name)
        return 200
    except Exception as e:
        print("Exception :", e)
        return 422 


