from sqlalchemy import insert, select, and_, or_, func

from app.bookings.dto import SBookingCreateDTO, SBookingDTO
from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.exceptions import RoomNotFoundException, RoomCannotBeBookedException
from app.hotels.rooms.dao import RoomDAO


class BookingDAO(BaseDAO[Bookings]):
    model = Bookings

    @classmethod
    async def get_qty_booked_room(cls, booking_data: SBookingCreateDTO) -> int:
        async with async_session_maker() as session:
            get_qty_booked_rooms = (
                select(func.count(Bookings.id))
                .where(
                    and_(
                        Bookings.room_id == booking_data.room_id,
                        or_(
                            and_(
                                Bookings.date_from >= booking_data.date_from,
                                Bookings.date_from <= booking_data.date_to,
                            ),
                            and_(
                                Bookings.date_from <= booking_data.date_from,
                                Bookings.date_to > booking_data.date_from,
                            ),
                        ),
                    )
                )
            )
            qty_booked_rooms = await session.execute(get_qty_booked_rooms)
            qty_booked_rooms: int = qty_booked_rooms.scalar()

            return qty_booked_rooms

    @classmethod
    async def create(cls, booking_data: SBookingCreateDTO) -> SBookingDTO:
        room = await RoomDAO.get_one_by_id(booking_data.room_id)
        if not room:
            raise RoomNotFoundException

        qty_booked_rooms: int = await cls.get_qty_booked_room(booking_data)

        if room.qty - qty_booked_rooms < 1:
            raise RoomCannotBeBookedException

        return await super().create(**booking_data.dict(), price=room.price)
