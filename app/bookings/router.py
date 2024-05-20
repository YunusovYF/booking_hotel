from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from app.bookings.dto import SBookingDTO, SBookingCreateDTO, SBookingCreateRequestDTO
from app.bookings.service import BookingService
from app.users.dependencies import get_current_user
from app.users.dto import SUserDTO

router = APIRouter(
    prefix='/bookings',
    tags=['bookings']
)


@router.post('')
async def create(
        booking_data: SBookingCreateRequestDTO,
        current_user: SUserDTO = Depends(get_current_user)
) -> SBookingDTO:
    booking_data = SBookingCreateDTO(**booking_data.dict(), user_id=current_user.id)
    return await BookingService.create(booking_data)


@router.get('')
@cache(expire=60)
async def get_all(current_user: SUserDTO = Depends(get_current_user)) -> list[SBookingDTO]:
    return await BookingService.get_all(user_id=current_user.id)


@router.get('/{booking_id}')
async def get_one_by_id(booking_id: int) -> SBookingDTO:
    return await BookingService.get_one_by_id(booking_id)


@router.get('/')
async def get_one_or_none(**args) -> SBookingDTO:
    return await BookingService.get_one_or_none(**args)
