from fastapi import APIRouter, Depends

from app.bookings.dao import BookingDAO
from app.bookings.dto import SBookingDTO, SBookingCreateDTO, SBookingCreateRequestDTO
from app.users.dependencies import get_current_user
from app.users.dto import SUserDTO

router = APIRouter(
    prefix='/bookings',
    tags=['bookings']
)


@router.get('')
async def get_all(current_user: SUserDTO = Depends(get_current_user)) -> list[SBookingDTO]:
    return await BookingDAO.get_all(user_id=current_user.id)


@router.get('/{booking_id}')
async def get_one_by_id(booking_id: int) -> SBookingDTO:
    return await BookingDAO.get_one_by_id(booking_id)


@router.get('/')
async def get_one_or_none(**args) -> SBookingDTO:
    return await BookingDAO.get_one_or_none(**args)


@router.post('')
async def create(
        booking_data: SBookingCreateRequestDTO,
        current_user: SUserDTO = Depends(get_current_user)
) -> SBookingDTO:
    booking_data = SBookingCreateDTO(**booking_data.dict(), user_id=current_user.id)
    return await BookingDAO.create(booking_data)
