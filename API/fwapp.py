"""This module contains the routes for the API.It contains the functions 
that are used to create the endpoints."""
from API import app
from API.services.db import *
from API.services.auth import *
from API.services.auth.utils import JWTBearer
from API.utils import scopes
from API.core.ExceptionHandlers import *
from API.core.Exceptions import *
from API.models import (UserAuth, UserOut, UseRefreshToken,
                        BulkSignup, FormData, TokenSchema, FrontendResponseModel)

from fastapi import Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

import datetime

# template and static files setup
templates = Jinja2Templates(directory="API/templates/")
app.mount("/static", StaticFiles(directory="API/static"), name="static")

# Middleware to handle CORS (cross origin  resource sharing) error in the browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Home"])
def _home(request: Request):
    # return templates.TemplateResponse("home.html", context={"request": request})
    return {"details": "Hello world!"}


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
        response_result["data"]['timestamp'] = f"{datetime.datetime.now()}"

    except Exception as e:
        print("Exception :", e)

    return response_result


@app.post("/api/post_data", response_model=FrontendResponseModel, dependencies=[Depends(JWTBearer())],
          tags=["Resource Server"])
def api_post_data(responses: FormData, user_credentials: str = Depends(JWTBearer())):
    response_result = {
        "status": "not_allowed",
        "message": ["Not authenticated"],
        "data": {},
    }
    user_creds = get_current_user_credentials(user_credentials)

    commit_to_db(response_result, responses, user_creds.AADHAR)
    return response_result


@app.get("/api/get_data", response_model=FrontendResponseModel, tags=["Resource Server"],
         dependencies=[Depends(JWTBearer())])
def api_get_data(village_name: str, user_credentials: str = Depends(JWTBearer())):
    response_result = {
        "status": "not_allowed",
        "message": ["Not authenticated"],
        "data": {},
    }
    user_creds = get_current_user_credentials(user_credentials)

    @scopes.init_checks(authorized_roles=["admin", "GOVTOff"], village_name=village_name,
                        response_result=response_result)
    def scoped_checks(user_creds: UserOut):
        if user_creds.role == 'admin':
            response_data = fetch_from_db(response_result, user_creds.village_name)
        else:
            response_data = fetch_from_db(response_result, village_name)
        return response_data['data']

    response_data = scoped_checks(user_creds)

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

    user_creds = get_current_user_credentials(user_credentials)

    @scopes.init_checks(authorized_roles=['admin', 'GOVTOff'], wrong_endpoint_roles=['GOVTOff'],
                        village_name=user_creds.village_name, response_result=response_result)
    def scoped_checks(user_creds: UserOut):
        pass

    scoped_checks(user_creds)

    familydata = fetch_familydata(response_result, user_creds.village_name, respondents_id)

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

    user_creds = get_current_user_credentials(user_credentials)

    @scopes.init_checks(authorized_roles=['admin', 'GOVTOff'], wrong_endpoint_roles=['GOVTOff'],
                        village_name=user_creds.village_name, response_result=response_result)
    def scoped_checks(user_creds: UserOut):
        pass

    scoped_checks(user_creds)

    indivdualdata = fetch_individualdata(response_result, user_creds.village_name, respondents_id)

    response_result['data'] = indivdualdata
    response_result['status'] = 'success'
    response_result['message'] = ['Authenticated']
    return response_result


@app.post('/auth/signup', summary="Create new user", response_model=FrontendResponseModel,
          tags=["Authorization Server"], dependencies=[Depends(JWTBearer())])
async def auth_signup(data: Union[UserAuth, BulkSignup], user_credentials: str = Depends(JWTBearer())):
    response_result = {
        "status": "not_allowed",
        "message": ["Not authenticated"],
        "data": {},
    }

    user_creds = get_current_user_credentials(user_credentials)

    @scopes.init_checks(authorized_roles=['admin', 'GOVTOff'],
                        village_name=data.village_name, response_result=response_result)
    def scoped_checks(user_creds: UserOut):
        if isinstance(data, UserAuth):
            if data.role not in ['admin', 'user']:
                raise AuthorizationFailedException(response_result, "not authorized")

            if data.role == 'admin' and user_creds.role == 'admin':
                raise AuthorizationFailedException(response_result, "not authorized")

        if user_creds.role == "admin" and data.village_name != user_creds.village_name:
            raise AuthorizationFailedException(response_result, "not authorized")

    scoped_checks(user_creds)

    signup(response_result, data)
    return response_result


@app.post('/auth/login', summary="Log-in to the user account", response_model=TokenSchema,
          tags=["Authorization Server"])
async def auth_login(form_data: UserAuth = Depends()):
    tokens = {
        "status": "Internal Server Error 500",
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


@app.get("/ops/get_village_list", summary="Get the list of village names", response_model=FrontendResponseModel,
         tags=["Sensitive ops"], dependencies=[Depends(JWTBearer())])
async def get_village_list(user_credentials: str = Depends(JWTBearer())):
    response_result = {
        "status": "not_allowed",
        "message": ["Not authenticated"],
        "data": {},
    }

    user_creds = get_current_user_credentials(user_credentials)

    @scopes.init_checks(authorized_roles=['GOVTOff'], response_result=response_result)
    def scoped_checks(user_creds: UserOut):
        pass

    scoped_checks(user_creds)

    village_list = get_available_villages(response_result)
    response_result['data']["village_names"] = village_list
    return response_result


# delete database route
@app.delete('/ops/delete_database', summary="Delete the database", tags=["Sensitive ops"],
            dependencies=[Depends(JWTBearer())])
async def ops_delete_database(dbname: str, user_credentials: str = Depends(JWTBearer())):
    response_result = {
        "status": "not_allowed",
        "message": ["Not authenticated"],
        "data": {},
    }

    user_creds = get_current_user_credentials(user_credentials)

    @scopes.init_checks(authorized_roles=['GOVTOff'], response_result=response_result, village_name=dbname)
    def scoped_checks(user_creds):
        pass

    scoped_checks(user_creds)

    delete_village_data(dbname, response_result)
    return response_result


@app.put('/ops/update_village_list', summary="Update the village list", tags=["Sensitive ops"],
         dependencies=[Depends(JWTBearer())])
async def ops_update_village_list(dbname: str, user_credentials: str = Depends(JWTBearer())):
    response_result = {
        "status": "not_allowed",
        "message": ["Not authenticated"],
        "data": {},
    }

    user_creds = get_current_user_credentials(user_credentials)

    @scopes.init_checks(authorized_roles=['GOVTOff'], response_result=response_result)
    def scoped_checks(user_creds):
        pass

    scoped_checks(user_creds)

    create_new_village(dbname, user_creds, response_result)
    return response_result

# @app.get('/auth/me', summary='Get details of currently logged in user', response_model=UserOut, tags=["SessionInfo"])
# async def get_me(user: str = Depends(JWTBearer())):
#     data = get_current_user_credentials(user)
#     return data
