from abc import ABC, abstractmethod
from typing import Any, Dict, List, Literal, Optional

from clickhouse_driver.dbapi import connect
from clickhouse_driver.dbapi.extras import DictCursor
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.results import DeleteResult, InsertOneResult, UpdateResult

from src.configs import Settings


class BaseRepo(ABC):
    @abstractmethod
    async def get(self, *args, **kwargs) -> List[Dict[str, Any]]:
        """Базовый метод для получения данных"""
        pass

    @abstractmethod
    async def post(self, *args, **kwargs):
        """Базовый метод для добавления записи в базу данных"""
        pass

    @abstractmethod
    async def delete(self, *args, **kwargs):
        """Базовый метод для удаления записей из базы данных"""
        pass

    @abstractmethod
    async def update(self, *args, **kwargs):
        """Базовый метод для изменения записи в базе данных"""
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

    async def post(self, target: str, data: dict, **kwargs) -> InsertOneResult:
        return await self.db[target].insert_one(data, **kwargs)

    async def delete(
        self,
        target: str,
        filter: Dict[str, Any],
        **kwargs,
    ) -> DeleteResult:
        """
        Удаляет документы из указанной коллекции MongoDB по заданным условиям.

        :param target: имя коллекции
        :param filter: словарь условий фильтрации
        :param data: новый объект
        :param kwargs: дополнительные параметры для delete_many
        :return: результат операции удаления
        """
        return await self.db[target].delete_one(filter, **kwargs)

    async def update(self, target: str, filter: dict,  data: dict, **kwargs) -> UpdateResult:
        return await self.db[target].update_one(filter, data, **kwargs)


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

    async def post(
        self,
        target: str,
        params: Dict[str, Any],
        **kwargs,
    ):
        """
        Выполняет вставку данных в указанную таблицу ClickHouse.

        :param target: имя таблицы
        :param data: данные для вставки в виде словаря
        :param kwargs: дополнительные параметры для выполнения запроса
        :return: пустой список (вставка в ClickHouse не возвращает данных)
        """
        columns = ", ".join(params.keys())
        placeholders = ", ".join([f"%({key})s" for key in params.keys()])
        query = f"INSERT INTO {target} ({columns}) VALUES ({placeholders})"

        with self.connection_pool as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params, **kwargs)

    async def delete(
        self,
        target: str,
        where_clause: str = "",
        params: Dict[str, Any] = {},
        **kwargs,
    ) -> bool:
        """
        Удаляет записи из таблицы ClickHouse по заданным условиям.

        :param target: имя таблицы
        :param where_clause: часть SQL после WHERE (без слова WHERE)
        :param params: параметры для безопасного выполнения
        :param kwargs: дополнительные параметры для execute()
        :return: True, если удаление прошло успешно
        :raises ValueError: если where_clause не указан
        """
        if not where_clause:
            raise ValueError("where_clause обязателен для операции DELETE в ClickHouse")

        query = f"ALTER TABLE {target} DELETE WHERE {where_clause}"
        with self.connection_pool as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params, **kwargs)

        return True

    async def update(
        self,
        target: str,
        update_data: Dict[str, Any],
        where_clause: str = "",
        params: Dict[str, Any] = {},
        **kwargs,
    ) -> bool:
        """
        Выполняет обновление записей в таблице ClickHouse.

        :param target: имя таблицы
        :param update_data: словарь с полями и их новыми значениями
        :param where_clause: часть SQL после WHERE (без слова WHERE)
        :param params: параметры для безопасного выполнения WHERE
        :param kwargs: дополнительные параметры для execute()
        :return: True, если обновление прошло успешно
        :raises ValueError: если where_clause не указан
        """
        if not where_clause:
            raise ValueError("where_clause обязателен для операции UPDATE в ClickHouse")

        set_clause = ", ".join([f"{key} = %({key})s" for key in update_data.keys()])
        query = f"ALTER TABLE {target} UPDATE {set_clause} WHERE {where_clause}"

        with self.connection_pool as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, {**params, **update_data}, **kwargs)

        return True
