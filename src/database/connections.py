from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any, Dict, Generator, List
from motor.motor_asyncio import AsyncIOMotorClient
from clickhouse_driver import connect

from configs import Settings

if TYPE_CHECKING:
    from clickhouse_driver.dbapi.connection import Connection

class BaseRepo(ABC):

    @abstractmethod
    async def create(self, *args, **kwargs): ...

    @abstractmethod
    async def read(self, *args, **kwargs): ...

    @abstractmethod
    async def update(self, *args, **kwargs): ...

    @abstractmethod
    async def delete(self, *args, **kwargs): ...


class AsyncMongoRepo(BaseRepo):
    def __init__(self, settings: Settings):
        self.mongo_client = AsyncIOMotorClient(settings.mongo_uri)
        self.db = self.mongo_client.get_default_database()

    async def disconnect(self):
        self.mongo_client.close()

    async def create(self, collection: str, item: dict, **kwargs):
        result = await self.db[collection].insert_one(item, **kwargs)
        return result.inserted_id

    async def read(self, collection: str, query: dict, **kwargs):
        return await self.db[collection].find_one(query, **kwargs)

    async def update(self, collection: str, query: dict, data: dict, **kwargs):
        return await self.db[collection].update_one(query, {"$set": data}, **kwargs)

    async def delete(self, collection: str, query: dict, **kwargs):
        return await self.db[collection].delete_one(query, **kwargs)

    async def find_many(self, collection: str, query: dict, **kwargs):
        cursor = self.db[collection].find(query, **kwargs)
        return await cursor.to_list(length=None)

    async def aggregate(self, collection: str, pipeline: list, **kwargs):
        cursor = self.db[collection].aggregate(pipeline, **kwargs)
        return await cursor.to_list(length=None)


class ClickHouseRepo(BaseRepo):
    def __init__(self, settings: Settings):
        self.clickhouse_uri = settings.clickhouse_uri

    @contextmanager
    def connect_db(self) -> Generator["Connection", Any, None]:
        with connect(host=self.clickhouse_uri) as conn:
            yield conn

    def create(self, table: str, data: List[Dict[str, Any]], **kwargs):
        """
        Вставка данных в таблицу.
        :param table: Название таблицы
        :param data: Список словарей (каждый — это строка для вставки)
        """
        if not data:
            return
        with self.connect_db.cursor() as cursor:

        columns = list(data[0].keys())
        rows = [tuple(item[col] for col in columns) for item in data]

        query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES"
        self.client.execute(query, rows, **kwargs)

    def read(self, query: str, params: Optional[tuple] = None, **kwargs) -> List[Dict]:
        """
        Выполнение произвольного SELECT-запроса.
        """
        result = self.client.execute(query, params=params, with_column_types=True, **kwargs)
        columns = [col[0] for col in result[1]]
        rows = result[0]
        return [dict(zip(columns, row)) for row in rows]

    def execute(self, query: str, params: Optional[tuple] = None, **kwargs) -> Any:
        """
        Выполнение произвольного запроса (например, INSERT/UPDATE/MUTATION).
        """
        return self.client.execute(query, params=params, **kwargs)

    def update(self, *args, **kwargs):
        raise NotImplementedError("ClickHouse не поддерживает UPDATE эффективно")

    def delete(self, *args, **kwargs):
        raise NotImplementedError("DELETE в ClickHouse ограничен")
