"""Custom Exception classes to update status messages and codes according to
different scenarios.

Custom Exceptions:
    VillageNotFoundException: If queried village is not found in the database.

    AuthorizationFailedException: If wrong endpoint or unauthorized access.

    InfoNotFoundException: If queried information not found in the database.

    ExistingUserException: If new account is attempted to create for
                           existing users.

    LoginFailedException: If credentials are not valid.

    DuplicateEntryException: If duplicate entry is attempted to store in the
                             database.
"""
import json

from API.models import TokenSchema, FrontendResponseModel


class VillageNotFoundException(Exception):
    def __init__(self, response_result: FrontendResponseModel, message: str):
        self.response_result = response_result
        self.message = message
        self.set_statuses()
        super(VillageNotFoundException, self).__init__(message)

    def set_statuses(self):
        self.response_result['status'] = 'abort'
        self.response_result['message'][0] = 'authenticated'
        self.response_result['message'].append('no such village exists in the database')

    def __repr__(self):
        return json.dumps(self.response_result)


class AuthorizationFailedException(Exception):
    def __init__(self, response_result: FrontendResponseModel, message: str):
        self.response_result = response_result
        self.message = message
        self.set_statuses()
        super(AuthorizationFailedException, self).__init__(message)

    def set_statuses(self):
        self.response_result['status'] = 'not_allowed'
        self.response_result['message'][0] = self.message

    def __repr__(self):
        return json.dumps(self.response_result)


class InfoNotFoundException(Exception):
    def __init__(self, response_result: FrontendResponseModel, message: str):
        self.response_result = response_result
        self.message = message
        self.set_statuses()
        super(InfoNotFoundException, self).__init__(message)

    def set_statuses(self):
        self.response_result['status'] = 'abort'
        self.response_result['message'][0] = 'authenticated'
        self.response_result['message'].append(self.message)

    def __repr__(self):
        return json.dumps(self.response_result)


class ExistingUserException(Exception):
    def __init__(self, response_result: FrontendResponseModel):
        self.response_result = response_result
        self.set_statuses()
        super(ExistingUserException, self).__init__()

    def set_statuses(self):
        self.response_result['status'] = f'failed'
        self.response_result['message'].append(f'user with this AADHAR Number already has an account')
        self.response_result['message'][0] = 'authenticated'

    def __repr__(self):
        return json.dumps(self.response_result)


class LoginFailedException(Exception):
    def __init__(self, token_result: TokenSchema):
        self.token_result = token_result
        self.set_statuses()
        super(LoginFailedException, self).__init__()

    def set_statuses(self):
        self.token_result['status'] = 'login_failed'

    def __repr__(self):
        return json.dumps(self.token_result)


class DuplicateEntryException(Exception):
    def __init__(self, response_result: FrontendResponseModel):
        self.response_result = response_result
        self.set_statuses()
        super(DuplicateEntryException, self).__init__()

    def set_statuses(self):
        self.response_result['status'] = 'abort'
        self.response_result['message'][0] = 'authenticated'
        self.response_result['message'].append('person(respondent) with this id already exists in the database')

    def __repr__(self):
        return json.dumps(self.response_result)
    
class DuplicateVillageException(Exception):
    def __init__(self, response_result: FrontendResponseModel):
        self.response_result = response_result
        self.set_statuses()
        super(DuplicateVillageException, self).__init__()

    def set_statuses(self):
        self.response_result['status'] = 'abort'
        self.response_result['message'][0] = 'authenticated'
        self.response_result['message'].append('Village already exists in the database')

    def __repr__(self):
        return json.dumps(self.response_result)    
    

