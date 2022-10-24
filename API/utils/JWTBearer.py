from ..core.ConfigEnv import settings
from ..models.AuthSchema import TokenPayload

from datetime import datetime

from fastapi import Request,HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import ValidationError
from jose import jwt



class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> str:
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            else:
                is_valid = JWTBearer.token_validation(credentials.credentials)
                if not is_valid:
                    raise HTTPException(status_code=403, detail="Invalid token or expired token.")
                return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    @staticmethod
    def token_validation(token: str) -> bool:
        try:
            payload = jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            token_data = TokenPayload(**payload)

            if datetime.fromtimestamp(token_data.exp) < datetime.now():
                return False

        except(jwt.JWTError, ValidationError):
            return False

        return True
