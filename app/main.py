from fastapi import FastAPI, Depends, HTTPException
# from sqlmodel import Session, select
from prometheus_fastapi_instrumentator import Instrumentator
from .models import models
# from .settings import settings
# from .utils import get_db
from .schemas import schemas
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated

async def startup(app):
    Instrumentator().instrument(app).expose(app)

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

dp_dependency = Annotated[Session, Depends(get_db)]

# Prometheus Metrics
startup(app)

# Healthcheck
@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}

# Create/Delete Cart
@app.post("/carts/", response_model=schemas.Cart)
def create_cart(cart: schemas.CartCreate, db: Session = Depends(get_db)): 
    # db_cart = db.query(models.Cart).filter(models.Cart.id == cart.id).first()
    db_cart = models.Cart(**cart.dict())
    # db_cart = models.Cart()
    # db_cart.user_id = user_id
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart

@app.delete("/carts/{cart_id}", response_model=None)
def delete_cart(cart_id: int, db: Session = Depends(get_db)):
    db_cart = db.get(models.Cart, cart_id)
    if not db_cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    db.delete(db_cart)
    db.commit()
    return

# Get items in cart
@app.get("/carts/{cart_id}", response_model=schemas.Cart)
def get_cart_items(cart_id: int, db: Session = Depends(get_db)):
    db_cart = db.query(models.Cart).filter(models.Cart.id == cart_id).first()
    if not db_cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return db_cart

# Add item to cart
@app.post("/carts/{cart_id}/items", response_model=schemas.Item)
def add_item_to_cart(cart_id: int, item_id: int, db: Session = Depends(get_db)):
    db_cart = db.get(models.Cart, cart_id)
    if not db_cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    db_item = db.get(models.Item, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.cart_id = cart_id
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# Create/Update/Get/Delete Item
@app.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.put("/items/{item_id}", response_model=schemas.Item)
def update_item(item_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = db.get(models.Item, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    item_data = item.dict(exclude_unset=True)
    for key, value in item_data.items():
        setattr(db_item, key, value)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items/{item_id}", response_model=schemas.Item)
def get_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.get(models.Item, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.delete("/items/{item_id}", response_model=schemas.Item)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.get(models.Item, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    if db_item.cart_id is not None:
        raise HTTPException(status_code=400, detail="Cannot delete item in cart")
    db.delete(db_item)
    db.commit()
    return
