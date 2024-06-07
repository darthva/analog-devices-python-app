from typing import Optional
from pydantic import BaseModel
from typing import ClassVar

class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: int

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    cart_id: int

    class Config:
        orm_mode = True

class CartBase(BaseModel):
    pass

class CartCreate(CartBase):
    pass

class CartItemRead(CartBase):
    cart_id: int

class Cart(CartBase):
    id: int
    items: list[CartItemRead] = []

    class Config:
        orm_mode = True
