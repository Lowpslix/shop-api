from datetime import datetime
from typing import List, Optional

from beanie import Document, Link, PydanticObjectId
from pydantic import BaseModel


class UserIn(BaseModel):
    username: str
    password: str


class CartItem(BaseModel):
    prodId: PydanticObjectId
    quantity: int


class User(Document):
    username: str
    hashed_password: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
    cart: List[CartItem] = []

    class Settings:
        name = "users"

    # class Config:
    #     schema_extra = {"example": {"name": "Adir Sellam", "email": "adir@gmail.test"}}
