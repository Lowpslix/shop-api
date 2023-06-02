from datetime import datetime
from typing import List, Optional

from beanie import Document, Link
from pydantic import BaseModel

from .product import Product
from .user import User


class OrderItem(BaseModel):
    product: Product
    quantity: int


class Order(Document):
    user: Link[User]
    products: List[OrderItem]

    class Settings:
        name = "orders"
