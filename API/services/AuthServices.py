"""Wrapper around different authentication and authorization methods.

Note that all the auth related routes redirect their control-flow via these
methods/functions to handle all the queries. In short, this collection of
methods/functions are essentially wrappers around the actual definitions.
"""
from jose import jwt

from API.utils.Auth import Auth
from ..core.ConfigEnv import settings
from ..core.Exceptions import *
from ..models.AuthSchema import UserOut, UserAuth, TokenPayload
from ..utils.DBQueries import DBQueries


def signup(response_result: FrontendResponseModel, data: UserAuth):
    """Wrapper method to handle signup process.

    Args:
        response_result: FrontendResponseModel. A TypedDict to return the
                         response captured from the API to the frontend.
        data: UserAuth. New user's prospective credentials from the frontend
                        to create their account.

    Raises:
        ExistingUserException: If account with entered AADHAR Number already exists.
    """
    # querying database to check if user already exist
    user = DBQueries.filtered_db_search("Auth", data.role, [], AADHAR=data.AADHAR_NO)
    if len(list(user)) != 0:
        # user with the entered credentials already exists
        raise ExistingUserException(response_result)

    userinfo = {
        'AADHAR': data.AADHAR_NO,
        'password': Auth.get_password_hash(data.password),
        'village_name': data.village_name,
    }
    DBQueries.insert_to_database("Auth", data.role, userinfo)  # saving user to database
    response_result['status'] = f'success'
    response_result['message'] = [f'User with this AADHAR NO created successfully']


def user_login(tokens: TokenSchema, form_data: UserAuth):
    """Wrapper method to handle sign-ins and generating `access_tokens`.

    Args:
        tokens: TokenSchema. A TypedDict to return `access_token`,
                             `refresh_access_tokens`, `status`, and `role`
                             related information to grant genuine users their
                             respective level of authorization according to
                             the maintained hierarchy.
        form_data: UserAuth. Sign-in credentials entered by the users at the
                             time of signing in.

    Raises:
        LoginFailedException: If no user with entered credentials exists.
    """
    user = DBQueries.filtered_db_search("Auth", form_data.role, ['_id'], AADHAR=form_data.AADHAR_NO)
    data = list(user)
    if len(data) == 0:
        # no such users in the database
        raise LoginFailedException(tokens)

    if not Auth.verify_password(form_data.password, data[0]['password']) or \
            not Auth.verify_village_name(data[0]['village_name'], form_data.village_name):
        # incorrect credentials
        raise LoginFailedException(tokens)

    # successful login
    sub = form_data.AADHAR_NO + "_" + form_data.role + "_" + form_data.village_name
    tokens['access_token'] = Auth.create_access_token(sub)
    tokens['refresh_token'] = Auth.create_refresh_token(sub)
    tokens['status'] = 'login successful'
    tokens['role'] = form_data.role


def get_current_user_credentials(token: str) -> UserOut:
    """Infers user's credentials by their authenticated `access_token`
    to help with scoping.

    Args:
        token: str. Authenticated `access_token` of the user.

    Returns:
        user: UserOut. Object of UserOut class depicting User's
                       `AADHAR Number` and `village_name`.
    """
    payload = jwt.decode(
        token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    token_data = TokenPayload(**payload)
    user_cred = token_data.sub.split("_")
    user = UserOut(AADHAR=user_cred[0], role=user_cred[1], village_name=user_cred[2])
    # user.AADHAR, user.role, user.village_name = user_cred

    return user


def get_role(token: str) -> str:
    """Infers user's role by their authenticated `access_token`
    to help with scoping.

    Args:
        token: str. Authenticated `access_token` of the user.

    Returns:
        role: Scope of the user.
    """
    payload = jwt.decode(
        token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    token_data = TokenPayload(**payload)
    role = token_data.sub.split("_")[1]
    return role


def handle_refresh_token_access(token: str) -> TokenSchema:
    """Wrapper method to implement rotating access tokens by validating
    current `refresh_access_token`.

    Args:
        token: A `refresh_access_token` from the user.

    Returns:
        A new pair of refresh_access and access tokens
    """
    return Auth.generate_access_tokens_from_refresh_tokens(token)
