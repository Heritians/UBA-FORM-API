from typing import Callable

from ..models.AuthSchema import UserOut
from .DBConnection import DBConnection
from ..core.Exceptions import *


def init_checks(**kwargs):
    def checks(specs: Callable):
        def wrapper_checks(role: str, creds: UserOut):
            if role not in kwargs["authorized_roles"]:
                raise AuthorizationFailedException(kwargs['response_result'], "not authorized")
            if 'wrong_endpoint_roles' in kwargs.keys() and role in kwargs['wrong_endpoint_roles']:
                raise AuthorizationFailedException(kwargs['response_result'], "wrong endpoint")
            if role == 'GOVTOff' and kwargs['village_name'] \
                    not in [db_names for db_names in
                            DBConnection.get_client().list_database_names() if
                            db_names not in ['Auth', 'string']]:
                raise VillageNotFoundException(kwargs['response_result'], "village not found in the DB")
            return specs(role, creds)
        return wrapper_checks
    return checks

