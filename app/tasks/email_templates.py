from email.message import EmailMessage

from pydantic import EmailStr

from app.bookings.dto import SBookingDTO
from app.config import settings


def create_booking_confirmation_email(booking: SBookingDTO, email_to: EmailStr) -> EmailMessage:
    email = EmailMessage()
    email['Subject'] = 'Booking confirmation'
    email['From'] = settings.SMTP_USER
    email['To'] = email_to

    email.set_content(
        f'''
            <h1>Booking confirmation</h1>
            <p>Dear {booking.date_from} {booking.date_to}</p>
        ''',
        subtype='html'
    )

    return email
