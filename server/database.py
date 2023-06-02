import os

from beanie import init_beanie
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

from server.models.order import Order
from server.models.product import Product
from server.models.user import User


async def init_db():
    client = AsyncIOMotorClient(os.environ["MONGODB"])

    await init_beanie(database=client.store, document_models=[User, Product, Order])
