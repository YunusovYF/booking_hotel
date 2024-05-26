from sqlalchemy import select, and_, or_, func
from sqlalchemy.exc import SQLAlchemyError

from app.bookings.dto import SBookingCreateDTO
from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.logger import logger


class BookingDAO(BaseDAO[Bookings]):
    model = Bookings

    @classmethod
    async def get_qty_booked_room(cls, booking_data: SBookingCreateDTO) -> int:
        try:
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
                get_qty_booked_rooms = await session.execute(get_qty_booked_rooms)
                qty_booked_rooms: int = get_qty_booked_rooms.scalar()

                return qty_booked_rooms
        except (SQLAlchemyError, Exception) as e:
            msg = 'Unknown'
            if isinstance(e, SQLAlchemyError):
                msg = 'Database'
            msg += ' Exc: Cannot get qty booked rooms'

            logger.error(
                msg,
                extra=booking_data.dict(),
                exc_info=True
            )
