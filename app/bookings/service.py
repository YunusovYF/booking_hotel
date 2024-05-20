from app.bookings.dao import BookingDAO
from app.bookings.dto import SBookingCreateDTO, SBookingDTO
from app.exceptions import RoomNotFoundException, RoomCannotBeBookedException
from app.hotels.rooms.dao import RoomDAO
from app.service.base import BaseService


class BookingService(BaseService):
    DAO = BookingDAO

    @classmethod
    async def create(cls, booking_data: SBookingCreateDTO) -> SBookingDTO:
        room = await RoomDAO.get_one_by_id(booking_data.room_id)
        if not room:
            raise RoomNotFoundException

        qty_booked_rooms: int = await cls.DAO.get_qty_booked_room(booking_data)

        if room.qty - qty_booked_rooms < 1:
            raise RoomCannotBeBookedException

        return await cls.DAO.create(**booking_data.dict(), price=room.price)
