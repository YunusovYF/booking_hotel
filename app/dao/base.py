from typing import TypeVar, Generic, List

from sqlalchemy import select

from app.database import async_session_maker

T = TypeVar('T')


class BaseDAO(Generic[T]):
    model: T = None

    @classmethod
    async def get_one_by_id(cls, model_id: int) -> T | None:
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(id=model_id)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def get_one_or_none(cls, *filter_by) -> T | None:
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter(*filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def get_all(cls, *filter_by) -> List[T] | []:
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter(*filter_by)
            result = await session.execute(query)
            return result.mappings().all()
