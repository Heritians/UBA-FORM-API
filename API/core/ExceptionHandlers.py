"""Exception Handlers to handle custom built exceptions.
"""
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi import status

from API import app

from .Exceptions import *


@app.exception_handler(VillageNotFoundException)
async def handle_village_not_found(request: Request, exec: VillageNotFoundException):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                        content=repr(exec)
                        )


@app.exception_handler(AuthorizationFailedException)
async def handle_not_authorized(request: Request, exec: AuthorizationFailedException):
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                        content=repr(exec)
                        )


@app.exception_handler(InfoNotFoundException)
async def handle_info_not_found(request: Request, exec: InfoNotFoundException):
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                        content=repr(exec)
                        )


@app.exception_handler(ExistingUserException)
async def handle_existing_user_found(request: Request, exec: ExistingUserException):
    return JSONResponse(status_code=status.HTTP_226_IM_USED,
                        content=repr(exec)
                        )


@app.exception_handler(LoginFailedException)
async def handle_login_failed(request: Request, exec: LoginFailedException):
    return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,
                        content=repr(exec)
                        )


@app.exception_handler(DuplicateEntryException)
async def handle_duplicate_entry(request: Request, exec: DuplicateEntryException):
    return JSONResponse(status_code=status.HTTP_409_CONFLICT,
                        content=repr(exec)
                        )

@app.exception_handler(DuplicateVillageException)
async def handle_duplicate_entry(request: Request, exec: DuplicateVillageException):
    return JSONResponse(status_code=status.HTTP_409_CONFLICT,
                        content=repr(exec)
                        )

