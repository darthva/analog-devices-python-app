from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True)

    items = relationship("Item", back_populates="owner")

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Integer, nullable=False)
    cart_id = Column(Integer, ForeignKey("carts.id"))

    owner = relationship("Cart", back_populates="items")

# class CartItem(Base):
#     __tablename__ = "cart_items"

#     id = Column(Integer, primary_key=True)
#     cart_id = Column(Integer, ForeignKey("carts.id"), nullable=False)
#     item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
#     quantity = Column(Integer, nullable=True, default=1)

#     cart = relationship("Cart", back_populates="items")
#     item = relationship("Item", back_populates="cart_items")