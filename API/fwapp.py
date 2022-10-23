from API import app
from API.services.DBManipulation import *
from API.services.AuthServices import *
from .models.RequestBodySchema import FormData
from .models.FrontendResponseSchema import FrontendResponseModel
from .models.EDAResponseSchema import EDAResponseData
from .models.AuthSchema import UserAuth, TokenSchema, SystemUser
from .utils.Auth import Auth

from fastapi.templating import Jinja2Templates
from fastapi import Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer


# template and static files setup
templates = Jinja2Templates(directory="API/templates/")
app.mount("/static", StaticFiles(directory="API/static"), name="static")

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)


@app.get("/")
@app.get("/home")
def home(request: Request):
    return templates.TemplateResponse("home.html", context={"request": request})


@app.get("/api/response_check",response_model=FrontendResponseModel)
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


@app.post("/api/post_data",response_model=FrontendResponseModel)
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

@app.get("/api/get_familydata",response_model=FrontendResponseModel)
def api_get_familydata(village_name:str,respondents_id: str):
    response_result = {
        "status": "not_allowed",
        "message": ["Not authenticated"],
        "data": {},
    }
    try:
        familydata=fetch_familydata(response_result, village_name,respondents_id)
        response_result['data']=familydata["data"]
        response_result['status'] = 'success'
        return response_result

    except Exception as e:
        response_result['status'] = 'error'
        print("Exception :", e)
        return response_result

@app.get("/api/get_individual_data",response_model=FrontendResponseModel)
def api_get_individual_data(village_name:str,respondents_id: str):
    response_result = {
        "status": "not_allowed",
        "message": ["Not authenticated"],
        "data": {},
    }
    try:
        indivdualdata=fetch_individualdata(response_result, village_name,respondents_id)
        response_result['data']=indivdualdata
        response_result['status'] = 'success'
        return response_result

    except Exception as e:
        response_result['status'] = 'error'
        print("Exception :", e)
        return response_result

@app.post('/signup', summary="Create new user", response_model=FrontendResponseModel)
async def create_user(data: UserAuth):
    response_result = {
        "status": "not_allowed",
        "message": ["Not authenticated"],
        "data": {},
    }
    try:
        signup(response_result,data)
        return response_result

    except Exception as e:
        response_result['status'] = 'error'
        print("Exception :", e)
        return response_result


@app.post('/login', summary="Log-in to the user account", response_model=TokenSchema)
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


@app.get('/me', summary='Get details of currently logged in user', response_model=UserOut)
async def get_me(user: SystemUser = Depends(Auth.get_current_user)):
    return user
