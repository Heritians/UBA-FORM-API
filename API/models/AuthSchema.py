from pydantic import BaseModel, Field
from typing import Union, List, Tuple


class TokenSchema(BaseModel):
    status: str
    access_token: str
    refresh_token: str
    role: str


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class UserAuth(BaseModel):
    AADHAR_NO: str = Field(..., description="user Aadhar number")
    password: str = Field(..., min_length=5, max_length=24, description="user password")
    village_name: str = Field(..., description="user village name")
    role: str = Field(..., description="user role")

class UserOut(BaseModel):
    AADHAR: str
    role: str
    village_name: str
    
class BulkSignup(BaseModel):
    AADHAR_NOS:Union[List[str],Tuple[str]]
    passwords:Union[List[str],Tuple[str]]
    village_name: str


class UseRefreshToken(BaseModel):
    refresh_access_token: str
