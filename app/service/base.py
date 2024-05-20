from typing import List


class BaseService:
    DAO = None

    @classmethod
    async def create(cls, **data):
        return await cls.DAO.create(**data)

    @classmethod
    async def get_one_by_id(cls, model_id: int):
        return await cls.DAO.get_one_by_id(model_id)

    @classmethod
    async def get_one_or_none(cls, **filter_by):
        return await cls.DAO.get_one_or_none(**filter_by)

    @classmethod
    async def get_all(cls, **filter_by):
        return await cls.DAO.get_all(**filter_by)

    @classmethod
    async def delete(cls, model_id: int) -> None:
        return await cls.DAO.delete(model_id)
