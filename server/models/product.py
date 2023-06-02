from datetime import datetime
from typing import Optional

from beanie import Document
from pydantic import BaseModel


class Product(Document):
    title: str
    price: float
    description: str
    imageUrl: str
    # userId: -> Link

    class Settings:
        name = "products"

    class Config:
        schema_extra = {
            "example": {
                "title": "book",
                "price": 10.99,
                "description": "A really nice book",
                "imageUrl": "https://example.com",
            }
        }


class UpdateProduct(BaseModel):
    title: Optional[str]
    price: Optional[float]
    description: Optional[str]
    imageUrl: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "title": "book",
                "price": 10.99,
                "description": "A really nice book",
                "imageUrl": "https://example.com",
            }
        }
