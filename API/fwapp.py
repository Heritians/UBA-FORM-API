"""This module contains the routes for the API.It contains the functions 
that are used to create the endpoints."""

from API import app
from API.services.DBManipulation import *
from API.services.AuthServices import *
from .models.RequestBodySchema import FormData
from .models.AuthSchema import UserAuth, TokenSchema, UserOut, UseRefreshToken
from .utils.JWTBearer import JWTBearer
from .utils import scopes
from .core.ExceptionHandlers import *
from .core.Exceptions import *

from fastapi.templating import Jinja2Templates
from fastapi import Request, Depends
from fastapi.staticfiles import StaticFiles

# template and static files setup
templates = Jinja2Templates(directory="API/templates/")
app.mount("/static", StaticFiles(directory="API/static"), name="static")


@app.get("/", tags=["Home"])
def home(request: Request):
    return templates.TemplateResponse("home.html", context={"request": request})


@app.get("/api/response_check", response_model=FrontendResponseModel, tags=["Resource Server"])
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
          tags=["Resource Server"])
def api_post_data(responses: FormData):
    response_result = {
        "status": "not_allowed",
        "message": ["Not authenticated"],
        "data": {},
    }

    commit_to_db(response_result, responses)
    return response_result


@app.get("/api/get_data", response_model=FrontendResponseModel, tags=["Resource Server"],        dependencies=[Depends(JWTBearer())])
def api_get_data(village_name: str, user_credentials: str = Depends(JWTBearer())):
    response_result = {
        "status": "not_allowed",
        "message": ["Not authenticated"],
        "data": {},
    }
    roles = get_role(user_credentials)
    user_creds = get_current_user_credentials(user_credentials)

    @scopes.init_checks(authorized_roles=["admin", "GOVTOff"], village_name=village_name,
                        response_result=response_result)
    def scoped_checks(roles: str, user_creds: UserOut):
        if roles == 'admin':
            response_data = fetch_from_db(response_result, user_creds['village_name'])
        else:
            response_data = fetch_from_db(response_result, village_name)
        return response_data['data']

    response_data = scoped_checks(roles, user_creds)

    response_result['data'] = response_data
    response_result['status'] = 'success'
    response_result['message'] = ['authorized']

    return response_result


@app.get("/api/get_familydata", response_model=FrontendResponseModel, tags=["Resource Server"],
         dependencies=[Depends(JWTBearer())])
def api_get_familydata(respondents_id: str, user_credentials: str = Depends(JWTBearer())):
    response_result = {
        "status": "not_allowed",
        "message": ["Not authenticated"],
        "data": {},
    }

    roles = get_role(user_credentials)
    creds = get_current_user_credentials(user_credentials)

    @scopes.init_checks(authorized_roles=['admin', 'GOVTOff'], wrong_endpoint_roles=['GOVTOff'],
                        village_name=creds['village_name'], response_result=response_result)
    def scoped_checks(roles: str, user_creds: UserOut):
        pass

    scoped_checks(roles, creds)

    familydata = fetch_familydata(response_result, creds['village_name'], respondents_id)

    response_result['data'] = familydata["data"]
    response_result['status'] = 'success'
    response_result['message'] = ['Authenticated']
    return response_result


@app.get("/api/get_individual_data", response_model=FrontendResponseModel, tags=["Resource Server"],
         dependencies=[Depends(JWTBearer())])
def api_get_individual_data(respondents_id: str, user_credentials: str = Depends(JWTBearer())):
    response_result = {
        "status": "not_allowed",
        "message": ["Not authenticated"],
        "data": {},
    }

    roles = get_role(user_credentials)
    creds = get_current_user_credentials(user_credentials)

    @scopes.init_checks(authorized_roles=['admin', 'GOVTOff'], wrong_endpoint_roles=['GOVTOff'],
                        village_name=creds['village_name'], response_result=response_result)
    def scoped_checks(roles: str, user_creds: UserOut):
        pass

    scoped_checks(roles, creds)

    indivdualdata = fetch_individualdata(response_result, creds['village_name'], respondents_id)

    response_result['data'] = indivdualdata
    response_result['status'] = 'success'
    response_result['message'] = ['Authenticated']
    return response_result


@app.post('/auth/signup', summary="Create new user", response_model=FrontendResponseModel, tags=["Authorization Server"],dependencies=[Depends(JWTBearer())])
async def create_user(data: UserAuth, user_credentials: str = Depends(JWTBearer())):
    response_result = {
        "status": "not_allowed",
        "message": ["Not authenticated"],
        "data": {},
    }

    roles = get_role(user_credentials)
    creds = get_current_user_credentials(user_credentials)

    @scopes.init_checks(authorized_roles=['admin', 'GOVTOff'],
                        village_name=data.village_name, response_result=response_result)
    def scoped_checks(roles: str, creds: UserOut):
        if data.role not in ['admin', 'user']:
            raise AuthorizationFailedException(response_result, "not authorized")

        if data.role == 'admin' and roles == 'admin':
            raise AuthorizationFailedException(response_result, "not authorized")

        if roles == "admin" and data.village_name != creds['village_name']:
            raise AuthorizationFailedException(response_result, "not authorized")

    scoped_checks(roles, creds)

    signup(response_result, data)
    return response_result


@app.post('/auth/login', summary="Log-in to the user account", response_model=TokenSchema, tags=["Authorization Server"])
async def login(form_data: UserAuth = Depends()):
    tokens = {
        "status": "Internal Server Error 505",
        "access_token": "",
        "refresh_token": "",
        "role": "unauthorized"
    }
    user_login(tokens, form_data)
    return tokens


@app.post("/auth/use_refresh_token", summary="generate a fresh pair of access tokens using refresh tokens",
          response_model=TokenSchema, tags=["Authorization Server"], dependencies=[Depends(JWTBearer())])
async def auth_use_refresh_token(existing_tokens: UseRefreshToken):
    return handle_refresh_token_access(existing_tokens.refresh_access_token)


# @app.get('/auth/me', summary='Get details of currently logged in user', response_model=UserOut, tags=["SessionInfo"])
# async def get_me(user: str = Depends(JWTBearer())):
#     data = get_current_user_credentials(user)
#     return data
