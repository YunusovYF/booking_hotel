import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin
from starlette.middleware.cors import CORSMiddleware

from app.bookings.admin import BookingsAdmin
from app.bookings.router import router as bookings_router
from app.config import settings
from app.database import engine
from app.images.router import router as images_router
from app.logger import logger
from app.pages.router import router as pages_router
from app.users.admin import UsersAdmin
from app.users.router import router as users_router

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(settings.REDIS_URL)
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield

app = FastAPI(lifespan=lifespan)

origins = settings.ORIGINS.split(";")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'OPTIONS', 'PUT', 'PATCH', 'DELETE'],
    allow_headers=['Content-Type', 'Set-Cookie', 'Access-Control-Allow-Headers',
                   'Access-Control-Allow-Origin', 'Authorization'],
)

app.mount('/static', StaticFiles(directory='app/static'), 'static')

app.include_router(users_router)
app.include_router(bookings_router)
app.include_router(pages_router)
app.include_router(images_router)

admin = Admin(app, engine)

admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    logger.info("Request handling time", extra={
        "process_time": round(process_time, 4)
    })
    return response
