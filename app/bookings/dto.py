from datetime import date

from pydantic import BaseModel


class SBookingCreateRequestDTO(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class SBookingCreateDTO(SBookingCreateRequestDTO):
    user_id: int


class SBookingDTO(SBookingCreateDTO):
    id: int
    price: int
    total_days: int
    total_cost: int
