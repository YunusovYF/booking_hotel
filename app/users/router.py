from fastapi import APIRouter, Response, Depends

from app.config import settings
from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.dao import UserDAO
from app.users.dependencies import get_current_user
from app.users.dto import SUserAuthDTO, SUserDTO

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@router.post('/register')
async def register_user(user_data: SUserAuthDTO) -> None:
    if await UserDAO.get_one_or_none(email=user_data.email):
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UserDAO.create(email=user_data.email, password=hashed_password)


@router.post('/login')
async def login_user(response: Response, user_data: SUserAuthDTO) -> SUserDTO:
    user = await authenticate_user(user_data)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({'sub': str(user.id)})
    response.set_cookie(settings.ACCESS_TOKEN_NAME, access_token, max_age=settings.ACCESS_TOKEN_EXPIRE)
    return user


@router.post('/logout')
async def logout_user(response: Response) -> None:
    response.delete_cookie(settings.ACCESS_TOKEN_NAME)


@router.post('/me')
async def read_user_me(current_user: SUserDTO = Depends(get_current_user)) -> SUserDTO:
    return current_user
