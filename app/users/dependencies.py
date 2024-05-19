from datetime import datetime, timezone

from fastapi import Request, Depends
from jose import JWTError, jwt

from app.config import settings
from app.exceptions import InvalidTokenException, TokenExpiredException, ValidateCredentialsException, \
    TokenAbsentException
from app.users.dao import UserDAO
from app.users.dto import SUserDTO


def get_token(request: Request) -> str:
    token = request.cookies.get(settings.ACCESS_TOKEN_NAME)
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)) -> SUserDTO:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except JWTError:
        raise InvalidTokenException

    expire: str = payload.get("exp")
    if (not expire) and (int(expire) < datetime.now(timezone.utc).timestamp()):
        raise TokenExpiredException

    user_id: str = payload.get("sub")
    if not user_id:
        raise ValidateCredentialsException

    user = await UserDAO.get_one_by_id(int(user_id))
    if not user:
        raise ValidateCredentialsException

    return user
