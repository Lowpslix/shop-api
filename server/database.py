from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from server.models.order import Order
from server.models.product import Product
from server.models.user import User


async def init_db():
    client = AsyncIOMotorClient(
        "mongodb+srv://adir9gg:yreZYjdgZv1OsLuH@cluster0.rpdcu7w.mongodb.net/?retryWrites=true&w=majority"
    )

    await init_beanie(database=client.store, document_models=[User, Product, Order])
