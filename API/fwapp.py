from API import app
from API.utils.DBConnection import DBConnection
from .RequestBodySchema import FormData, Test

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

    return json.dumps(response_result)


@app.post("/api/post_data")
async def api_post_data(responses: Test):
    return {'test': 'success'}
