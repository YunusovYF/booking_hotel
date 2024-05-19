from fastapi import FastAPI

from app.bookings.router import router as bookings_router
from app.users.router import router as users_router
from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users


app = FastAPI()

app.include_router(users_router)
app.include_router(bookings_router)
