from typing import TypeVar, Generic, List

from sqlalchemy import select, insert, delete

from app.database import async_session_maker

T = TypeVar('T')


class BaseDAO(Generic[T]):
    model: T = None

    @classmethod
    async def create(cls, **data) -> T:
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model.__table__.columns)
            result = await session.execute(query)
            await session.commit()
            return result.mappings().one()

    @classmethod
    async def get_one_by_id(cls, model_id: int) -> T | None:
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(id=model_id)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def get_one_or_none(cls, **filter_by) -> T | None:
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def get_all(cls, **filter_by) -> List[T] | []:
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def delete(cls, model_id: int) -> None:
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(id=model_id)
            await session.execute(query)
            await session.commit()
