"""Decorator to apply scope related initial checks to ensure right
authorization barrier coherent to the 3-layered maintained hierarchy. Any
request made to secured endpoints will first be redirected here to perform
these checks.

Args:
    specs: Callable. A function performing Route-specific scope checks.

Possible kwargs:
    authorized_roles: List[str]. List of roles that have an authorized access
                                 to any particular routes.
    response_result: Optional[FrontendResponseModel]. Response model to pass to
                     custom exceptions unauthorized user tries to access the
                     endpoint to make appropriate changes in error messages and
                     status codes.
    village_name: Optional[str]. Name of the village if applicable.
    wrong_endpoint_roles: Optional[List[str]]. List of roles that have an
                          authorized access to but wrong endpoint access to
                          any particular route.

Raises:
    AuthorizationFailedException: If Wrong endpoint or unauthorized access.
    VillageNotFoundException: If queried village is not found in the database.

"""
from typing import Callable

from ..models.AuthSchema import UserOut
from ..services import DBManipulation
from ..core.Exceptions import *


def init_checks(**kwargs) -> Callable:
    def checks(specs: Callable) -> Callable:
        def wrapper_checks(creds: UserOut):
            if creds.role not in kwargs["authorized_roles"]:
                raise AuthorizationFailedException(kwargs['response_result'], "not authorized")
            if 'wrong_endpoint_roles' in kwargs.keys() and creds.role in kwargs['wrong_endpoint_roles']:
                raise AuthorizationFailedException(kwargs['response_result'], "wrong endpoint")
            if creds.role == 'GOVTOff' and "village_name" in kwargs and kwargs['village_name'] \
                    not in DBManipulation.get_available_villages(kwargs["response_result"]):
                raise VillageNotFoundException(kwargs['response_result'], "village not found in the DB")
            return specs(creds)

        return wrapper_checks

    return checks
