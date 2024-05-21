import asyncio
import smtplib
from pathlib import Path

from PIL import Image

from app.bookings.dao import BookingDAO
from app.config import settings
from app.tasks.celery_config import celery_app
from app.tasks.email_templates import create_booking_confirmation_email
from app.users.dao import UserDAO


@celery_app.task
def process_pic(path: str):
    im_path = Path(path)
    im = Image.open(im_path)
    im_resized_300 = im.resize((300, 300))
    im_resized_300.save(f'app/static/images/300_{im_path.name}')


async def send_booking_confirmation_email_task(booking_id: int):
    booking = await BookingDAO.get_one_by_id(booking_id)
    user = await UserDAO.get_one_by_id(booking.user_id)
    msg_content = create_booking_confirmation_email(booking, user.email)
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)


@celery_app.task
def send_booking_confirmation_email(booking_id: int):
    asyncio.run(send_booking_confirmation_email_task(booking_id))
