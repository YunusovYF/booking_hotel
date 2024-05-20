from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from app.bookings.dto import SBookingDTO
from app.bookings.router import get_all

router = APIRouter(
    prefix='/pages',
    tags=['pages']
)
templates = Jinja2Templates(directory='app/templates')

@router.get('/hotels')
async def get_hotels_page(
        request: Request,
        bookings: list[SBookingDTO] = Depends(get_all)
):
    return templates.TemplateResponse(
        'hotels.html',
        {
            'request': request,
            'bookings': bookings
        }
    )
