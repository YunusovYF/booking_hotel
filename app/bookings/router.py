from fastapi import APIRouter

from app.bookings.dao import BookingDAO
from app.bookings.dto import SBookingsDTO

router = APIRouter(
    prefix='/bookings',
    tags=['bookings']
)


@router.get('')
async def get_all() -> list[SBookingsDTO]:
    return await BookingDAO.get_all()


@router.get('/{booking_id}')
async def get_one_by_id(booking_id: int) -> SBookingsDTO:
    return await BookingDAO.get_one_by_id(booking_id)


@router.get('/{*args}')
async def get_one_or_none(*args) -> SBookingsDTO:
    return await BookingDAO.get_one_or_none(*args)
