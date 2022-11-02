"""Utility class to leverage encryption, verification of entered credentials
and generation of JWT access tokens.
"""
from datetime import datetime, timedelta
from typing import Union, Any

from jose import jwt
from passlib.context import CryptContext
from pydantic import ValidationError

from ..core.ConfigEnv import settings
from..core.Exceptions import *
from ..models.AuthSchema import TokenPayload


ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days


class Auth:
    """Utility class to perform -  1.encryption via `bcrypt` scheme.
    2.password hashing 3.verification of credentials and generating
    access tokens.

    Attrs:
        pwd_context: CryptContext. Helper for hashing & verifying passwords
                                   using `bcrypt` algorithm.
    """
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def get_password_hash(cls,password):
        return cls.pwd_context.hash(password)

    @classmethod    
    def verify_password(cls, plain_password, hashed_password):
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def verify_village_name(cls, entered_village_name, db_village_name):
        return entered_village_name == db_village_name

    @staticmethod    
    def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
        if expires_delta is not None:
            expires_delta = datetime.utcnow() + expires_delta
        else:
            expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.ALGORITHM)
        return encoded_jwt

    @staticmethod    
    def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
        if expires_delta is not None:
            expires_delta = datetime.utcnow() + expires_delta
        else:
            expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
        
        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, settings.JWT_REFRESH_SECRET_KEY, settings.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def generate_access_tokens_from_refresh_tokens(token: str):
        tokens = {
            "status": "Internal Server Error 505",
            "access_token": "",
            "refresh_token": "",
            "role": "unauthorized"
        }
        try:
            payload = jwt.decode(
                token, settings.JWT_REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            token_data = TokenPayload(**payload)
        except (jwt.JWTError, ValidationError):
            raise LoginFailedException(tokens)
        tokens['access_token'] = Auth.create_access_token(token_data.sub)
        tokens['refresh_token'] = Auth.create_refresh_token(token_data.sub)
        tokens['status'] = 'login successful'
        tokens['role'] = token_data.sub.split("_")[1]
        return tokens


