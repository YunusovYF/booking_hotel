from sqladmin import ModelView

from app.bookings.models import Bookings


class BookingsAdmin(ModelView, model=Bookings):
    column_list = '__all__'
    name = 'Booking'
    name_plural = 'Bookings'
