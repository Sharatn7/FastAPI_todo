from typing import Any, List, Optional
from beanie import init_beanie, PydanticObjectId
from models.todo import Todo
from motor.motor_asyncio import AsyncIOMotorClient  # MongoDB driver
from pydantic import BaseSettings, BaseModel


class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None

    async def initialize_database(self):
        client = AsyncIOMotorClient(self.DATABASE_URL)
        await init_beanie(database=client.get_default_database(),
                          document_models=[Todo])

    class Config:
        env_file = ".env"


class Database:
    def __init__(self, model):
        self.model = model

    async def save(self, document) -> None:
        await document.create()
        return

    async def get(self, id: PydanticObjectId) -> Any:
        doc = await self.model.get(id)
        if doc:
            return doc
        return False

    async def get_all(self) -> List[Any]:
        docs = await self.model.find_all().to_list()
        return docs

    async def update(self, id: PydanticObjectId, data: dict) -> Any:
        task = await self.model.find_one({"_id": id})
        if not task:
            return False
        if task:
            updated_task = await task.update({"$set": data})
            return True

    async def delete(self, id: PydanticObjectId) -> Any:
        doc = await self.get(id)
        if not doc:
            return False
        await doc.delete()
        return True
