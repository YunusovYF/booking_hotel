from datetime import date

from fastapi import FastAPI, Query, Depends
from pydantic import BaseModel

app = FastAPI()


class SHotel(BaseModel):
    address: str
    name: str
    stars: int
    has_spa: bool


class HotelsSearchArgs:
    def __init__(
            self,
            location: str,
            date_from: date,
            date_to: date,
            stars: int = Query(None, ge=1, le=5),
            has_spa: bool = Query(None),
    ):
        self.location = location
        self.date_from = date_from
        self.date_to = date_to
        self.stars = stars
        self.has_spa = has_spa


@app.get('/hotels', response_model=list[SHotel])
def get_hotels(
        search_args: HotelsSearchArgs = Depends()
):
    hotels = [
        {
            'address': '123 Main Street',
            'name': 'Hotel California',
            'stars': 4,
        }
    ]

    return hotels


class SBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date


@app.post('/bookings')
def add_booking(booking: SBooking):
    return {'message': f'{booking = }'}
