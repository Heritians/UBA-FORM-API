from API import app
from API.utils.DBConnection import DBConnection
from API.services.DBManipulation import *
from .RequestBodySchema import FormData
from .ResponseBodySchema import EDAResponseData

from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.staticfiles import StaticFiles

# template and static files setup
templates = Jinja2Templates(directory="API/templates/")
app.mount("/static", StaticFiles(directory="API/static"), name="static")


@app.get("/")
@app.get("/home")
def home(request: Request):
    return templates.TemplateResponse("home.html", context={"request": request})


@app.get("/api/response_check")
def api_response_check():
    response_result = {
        "status": "not_allowed",
        "message": ["Not authenticated"],
        "data": {},
    }
    try:
        db_msg = ""
        if DBConnection.flag:
            db_msg = "Connection Successful to db!"
        else:
            db_msg = "Connection failed to db"

        response_result["message"].append(db_msg)

    except Exception as e:
        print("Exception :", e)

    return response_result


@app.post("/api/post_data")
def api_post_data(responses: FormData):
    response_result = {
        "status": "not_allowed",
        "message": ["Not authenticated"],
        "data": {},
    }
    try:
        commit_to_db(response_result, responses)
        return response_result
    except Exception as e:
        print("Exception :", e)
        return 422


@app.get("/api/get_data", response_model=EDAResponseData)
def api_get_data(village_name: str):
    response_result = {
        "status": "not_allowed",
        "message": ["Not authenticated"],
        "data": {},
    }
    try:
        response_data = fetch_from_db(response_result, village_name)
        return response_data["data"]
    except Exception as e:
        print("Exception :", e)
        return 422

@app.get("/api/get_familydata")
def api_get_familydata(village_name:str,respondents_id: str):
    response_result = {
        "status": "not_allowed",
        "message": ["Not authenticated"],
        "data": {},
    }
    try:
        familydata=fetch_familydata(response_result, village_name,respondents_id)
        return familydata["data"]

    except Exception as e:
        print("Exception :", e)
        return 422


