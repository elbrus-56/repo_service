from abc import ABC, abstractmethod
from typing import Any, Dict, List, Literal, Optional

from clickhouse_driver.dbapi import connect
from clickhouse_driver.dbapi.extras import DictCursor
from motor.motor_asyncio import AsyncIOMotorClient

from src.configs import Settings


class BaseRepo(ABC):
    @abstractmethod
    async def get(self, *args, **kwargs) -> List[Dict[str, Any]]:
        """Базовый метод для получения данных"""
        pass


class MongoRepo(BaseRepo):
    def __init__(self, client: AsyncIOMotorClient):
        self.client = client
        self.db = self.client.get_database()

    async def get(
        self,
        target: str,
        order_by: Optional[str] = None,
        sort: Literal[1, -1] = 1,
        limit: int = 0,
        offset: int = 0,
        filter: Dict[str, Any] = {},
        projection: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> List[Dict[str, Any]]:
        """
        Получение данных из MongoDB
        :param target: имя коллекции
        :param query: словарь с условиями поиска
        :param projection: какие поля возвращать (опционально)
        :param kwargs: дополнительные параметры для find()
        :return: список документов
        """
        cursor = self.db[target].find(filter, projection, **kwargs)
        if offset:
            cursor = cursor.skip(offset)
        if limit:
            cursor = cursor.limit(limit)
        if order_by:
            cursor.sort({order_by: int(sort)})
        return [doc async for doc in cursor]


class ClickHouseRepo(BaseRepo):
    def __init__(self, settings: Settings):
        self.connection_pool = connect(settings.clickhouse_uri)

    async def get(
        self,
        target: str,
        where_clause: str = "",
        params: dict = {},
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[str] = None,
        sort: Literal["ASC", "DESC"] = "ASC",
        **kwargs,
    ) -> List[Dict[str, Any]]:
        """
        Получение данных из ClickHouse
        :param target: имя таблицы
        :param where_clause: часть SQL после WHERE (без слова WHERE)
        :param params: параметры для безопасного выполнения
        :param limit: ограничение количества строк
        :return: список строк как словарей
        """
        query = f"SELECT * FROM {target}"
        if where_clause:
            query += f" WHERE {where_clause}"
        if order_by:
            query += f" ORDER BY {order_by} {sort}"
        if limit:
            query += f" LIMIT {limit}"
        if offset:
            query += f" OFFSET {offset}"

        with self.connection_pool as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, params, **kwargs)
                return cursor.fetchall()
