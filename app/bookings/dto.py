from datetime import date

from pydantic import BaseModel


class SBookingsCreateDTO(BaseModel):
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int


class SBookingsDTO(SBookingsCreateDTO):
    id: int
    total_days: int
    total_cost: int
