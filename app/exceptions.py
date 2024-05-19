from typing import Optional

from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self, detail: Optional[str] = None):
        super().__init__(status_code=self.status_code, detail=detail or self.detail)


class UserAlreadyExistsException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'User with this email already exists'


class IncorrectEmailOrPasswordException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Incorrect email or password'


class TokenAbsentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Token absent'


class InvalidTokenException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Invalid token'


class TokenExpiredException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Token expired'


class ValidateCredentialsException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Could not validate credentials'


class NotAuthenticatedException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Not authenticated'


class RoomNotFoundException(BookingException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Room not found'


class RoomCannotBeBookedException(BookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Room cannot be booked'
