from fastapi import BackgroundTasks

from app.bookings.dao import BookingDAO
from app.bookings.dto import SBookingCreateDTO, SBookingDTO
from app.exceptions import RoomNotFoundException, RoomCannotBeBookedException
from app.hotels.rooms.dao import RoomDAO
from app.service.base import BaseService

from app.tasks.tasks import send_booking_confirmation_email, send_booking_confirmation_email_task


class BookingService(BaseService):
    DAO = BookingDAO

    @classmethod
    async def create(cls, booking_data: SBookingCreateDTO, background_tasks: BackgroundTasks) -> SBookingDTO:
        room = await RoomDAO.get_one_by_id(booking_data.room_id)
        if not room:
            raise RoomNotFoundException

        qty_booked_rooms: int = await cls.DAO.get_qty_booked_room(booking_data)

        if room.qty - qty_booked_rooms < 1:
            raise RoomCannotBeBookedException

        booking = await cls.DAO.create(**booking_data.dict(), price=room.price)

        send_booking_confirmation_email.delay(booking.id)

        background_tasks.add_task(send_booking_confirmation_email_task, booking.id)

        return booking
