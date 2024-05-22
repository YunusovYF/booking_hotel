from sqlalchemy import select, and_, or_, func

from app.bookings.dto import SBookingCreateDTO
from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker


class BookingDAO(BaseDAO[Bookings]):
    model = Bookings

    @classmethod
    async def get_qty_booked_room(cls, booking_data: SBookingCreateDTO) -> int:
        async with async_session_maker() as session:
            get_qty_booked_rooms = (
                select(func.count(cls.model.id))
                .where(
                    and_(
                        cls.model.room_id == booking_data.room_id,
                        or_(
                            and_(
                                cls.model.date_from >= booking_data.date_from,
                                cls.model.date_from <= booking_data.date_to,
                            ),
                            and_(
                                cls.model.date_from <= booking_data.date_from,
                                cls.model.date_to > booking_data.date_from,
                            ),
                        ),
                    )
                )
            )
            qty_booked_rooms = await session.execute(get_qty_booked_rooms)
            qty_booked_rooms: int = qty_booked_rooms.scalar()

            return qty_booked_rooms
