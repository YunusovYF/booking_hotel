import asyncio
import json

import pytest
from sqlalchemy import insert

from app.config import settings
from app.database import engine, Base, async_session_maker

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.main import app
from app.users.models import Users
from httpx import AsyncClient


@pytest.fixture(scope="session", autouse=True)
async def prepare_db():
    assert settings.MODE =='TEST'

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f'app/tests/mock_{model}.json', 'r', encoding='utf-8') as file:
            return json.load(file)

    users = open_mock_json('users')
    hotels = open_mock_json('hotels')
    rooms = open_mock_json('rooms')
    bookings = open_mock_json('bookings')

    async with async_session_maker() as session:
        add_users = insert(Users).values(users)
        add_hotels = insert(Hotels).values(hotels)
        add_rooms = insert(Rooms).values(rooms)
        add_bookings = insert(Bookings).values(bookings)

        await session.execute(add_users)
        await session.execute(add_hotels)
        await session.execute(add_rooms)
        await session.execute(add_bookings)
        await session.commit()


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='function')
async def ac():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope='session')
async def authenticated_ac():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post('/users/login', json={'email': 'test@test.com', 'password': 'test'})
        assert ac.cookies['booking_access_token']
        yield ac

@pytest.fixture(scope='function')
async def session():
    async with async_session_maker() as session:
        yield session
