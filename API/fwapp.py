from API import app
from API.services.DBManipulation import *
from API.services.AuthServices import *
from .models.RequestBodySchema import FormData
from .models.FrontendResponseSchema import FrontendResponseModel
from .models.AuthSchema import UserAuth, TokenSchema, UserOut
from .utils.JWTBearer import JWTBearer

from fastapi.templating import Jinja2Templates
from fastapi import Request, Depends
from fastapi.staticfiles import StaticFiles

# template and static files setup
templates = Jinja2Templates(directory="API/templates/")
app.mount("/static", StaticFiles(directory="API/static"), name="static")


@app.get("/", tags=["Home"])
@app.get("/home", tags=["Home"])
def home(request: Request):
    return templates.TemplateResponse("home.html", context={"request": request})


@app.get("/api/response_check", response_model=FrontendResponseModel, tags=["Frontend Response"])
def api_response_check():
    response_result = {
        "status": "not_allowed",
        "message": ["Not authenticated"],
        "data": {},
    }
    try:
        db_msg = ""
        if get_db_conn_flag():
            db_msg = "Connection Successful to db!"
        else:
            db_msg = "Connection failed to db"

        response_result["message"].append(db_msg)

    except Exception as e:
        print("Exception :", e)

    return response_result


@app.post("/api/post_data", response_model=FrontendResponseModel, dependencies=[Depends(JWTBearer())],
          tags=["Frontend Response"])
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
        response_result['status'] = 'error'
        print("Exception :", e)
        return response_result


@app.get("/api/get_data", response_model=FrontendResponseModel, tags=["EDA Response"],
         dependencies=[Depends(JWTBearer())])
def api_get_data(village_name: str, user_credentials: str = Depends(JWTBearer())):
    response_result = {
        "status": "not_allowed",
        "message": ["Not authenticated"],
        "data": {},
    }
    try:
        roles = get_role(user_credentials)
        user_creds = get_current_user_credentials(user_credentials)

        if roles == "user":
            response_result["message"] = ["Not authorized"]
            return response_result

        response_data = None
        if roles == 'admin':
            response_data = fetch_from_db(response_result, user_creds['village_name'])

        else:

            if village_name not in [db_names for db_names in DBConnection.get_client().list_database_names() if
                                    db_names not in ['Auth', 'string']]:
                raise ValueError("VillageName not found")
            response_data = fetch_from_db(response_result, village_name)

        response_result['data'] = response_data['data']
        response_result['status'] = 'success'
        response_result['message'] = ['authorized']

        return response_result

    except Exception as e:
        print("Exception :", e)
        response_result["status"] = "500"
        response_result["message"] = ["Internal Server Error"]
        return response_result


@app.get("/api/get_familydata", response_model=FrontendResponseModel, tags=["Frontend Response"],
         dependencies=[Depends(JWTBearer())])
def api_get_familydata(respondents_id: str, user_credentials: str = Depends(JWTBearer())):
    response_result = {
        "status": "not_allowed",
        "message": ["Not authenticated"],
        "data": {},
    }

    roles = get_role(user_credentials)
    if roles == "user":
        response_result["message"] = ["Not authorized"]
        return response_result

    elif roles == "GOVTOff":
        response_result["message"] = ["Wrong endpoint"]
        return response_result

    village_name = get_current_user_credentials(user_credentials)['village_name']

    try:
        familydata = fetch_familydata(response_result, village_name, respondents_id)
        response_result['data'] = familydata["data"]
        response_result['status'] = 'success'
        return response_result

    except Exception as e:
        response_result['status'] = 'error'
        print("Exception :", e)
        return response_result


@app.get("/api/get_individual_data", response_model=FrontendResponseModel, tags=["Frontend Response"],
         dependencies=[Depends(JWTBearer())])
def api_get_individual_data(respondents_id: str, user_credentials: str = Depends(JWTBearer())):
    response_result = {
        "status": "not_allowed",
        "message": ["Not authenticated"],
        "data": {},
    }

    roles = get_role(user_credentials)
    if roles == "user":
        response_result["message"] = ["Not authorized"]
        return response_result

    elif roles == "GOVTOff":
        response_result["message"] = ["Wrong endpoint"]
        return response_result

    village_name = get_current_user_credentials(user_credentials).village_name

    try:
        indivdualdata = fetch_individualdata(response_result, village_name, respondents_id)
        response_result['data'] = indivdualdata
        response_result['status'] = 'success'
        return response_result

    except Exception as e:
        response_result['status'] = 'error'
        print("Exception :", e)
        return response_result


@app.post('/signup', summary="Create new user", response_model=FrontendResponseModel, tags=["Auth"],
          dependencies=[Depends(JWTBearer())])
async def create_user(data: UserAuth, user_credentials: str = Depends(JWTBearer())):
    response_result = {
        "status": "not_allowed",
        "message": ["Not authenticated"],
        "data": {},
    }

    roles = get_role(user_credentials)
    if roles == "user":
        response_result["message"] = ["Not authorized"]
        return response_result

    try:
        signup(response_result, data)
        return response_result

    except Exception as e:
        response_result['status'] = 'error'
        print("Exception :", e)
        return response_result


@app.post('/login', summary="Log-in to the user account", response_model=TokenSchema, tags=["Auth"])
async def login(form_data: UserAuth = Depends()):
    tokens = {
        "status": "Internal Server Error 505",
        "access_token": "",
        "refresh_token": "",
        "role": "unauthorized"
    }
    try:
        user_login(tokens, form_data)
        return tokens

    except Exception as e:
        print("Exception :", e)
        return tokens


@app.get('/me', summary='Get details of currently logged in user', response_model=UserOut, tags=["SessionInfo"])
async def get_me(user: str = Depends(JWTBearer())):
    data = get_current_user_credentials(user)
    return data
