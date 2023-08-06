"""Utility class to leverage encryption, verification of entered credentials
and generation of JWT access tokens.
"""
from datetime import datetime, timedelta
from typing import Union, Any

from jose import jwt
from passlib.context import CryptContext
from pydantic import ValidationError

from API.core.ConfigEnv import settings
from API.core.Exceptions import *
from API.models import TokenPayload, TokenSchema

from fastapi.exceptions import HTTPException


ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 3 # 3 hours


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
    def get_password_hash(cls,password: str) -> str:
        """Encrypts the entered password.

        Args:
            password: str. Entered password.

        Returns:
            returns hashed(encrypted) password string.
        """
        return cls.pwd_context.hash(password)

    @classmethod    
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        """Validates if the entered password matches the actual password.

        Args:
            plain_password: str. Entered password by user.
            hashed_password: str. hashed password from the database.

        Returns:
            bool value indicating whether the passwords match or not.
        """
        return cls.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def verify_village_name(entered_village_name: str, db_village_name: str) -> bool:
        """Validates if the entered password matches the actual password.

        Args:
            entered_village_name: str. Entered `village_name` by user.
            db_village_name: str. village_name from the database.

        Returns:
            bool value indicating whether the village names match or not.
        """
        return entered_village_name == db_village_name

    @staticmethod
    def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
        """Creates JWT access token.

        Args:
            subject: Union[Any, str]. Hash_key to generate access token from.
            expires_delta: int = None. Expiry time for the JWT.

        Returns:
            encoded_jwt: str. Encoded JWT token from the subject of interest.
        """
        if expires_delta is not None:
            expires_delta = datetime.utcnow() + expires_delta
        else:
            expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.ALGORITHM)
        return encoded_jwt

    @staticmethod    
    def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
        """Creates JWT refresh access token.

        Args:
            subject: Union[Any, str]. Hash_key to generate access token from.
            expires_delta: int = None. Expiry time for the JWT.

        Returns:
            encoded_jwt: str. Encoded JWT token from the subject of interest.
        """
        if expires_delta is not None:
            expires_delta = datetime.utcnow() + expires_delta
        else:
            expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
        
        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, settings.JWT_REFRESH_SECRET_KEY, settings.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def generate_access_tokens_from_refresh_tokens(token: str) -> TokenSchema:
        """Generates a new pair of tokens by implementing rotating
        refresh_access_tokens.

        Args:
            token: str. Current valid refresh access token.

        Returns:
            tokens: TokenSchema. New tokens with new validity.

        Raises:
            LoginFailedException: If the current refresh access token is
                                  invalid.
        """
        tokens = {
            "status": "Internal Server Error 500",
            "access_token": "",
            "refresh_token": "",
            "role": "unauthorized"
        }
        try:
            payload = jwt.decode(
                token, settings.JWT_REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            token_data = TokenPayload(**payload)
            if datetime.fromtimestamp(token_data.exp)< datetime.now():
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
        except (jwt.JWTError, ValidationError):
            raise LoginFailedException(tokens)
        tokens['access_token'] = Auth.create_access_token(token_data.sub)
        tokens['refresh_token'] = token # Do not generate new `REFRESH_ACCESS_TOKEN`, instead, return the original
        tokens['status'] = 'login successful'
        tokens['role'] = token_data.sub.split("_")[1]
        return tokens


