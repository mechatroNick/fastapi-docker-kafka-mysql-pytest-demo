from sqlalchemy.orm import Session
from ddtrace import tracer
import models
import schemas


@tracer.wrap(name=f"{__name__}.get_items()")
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


@tracer.wrap(name=f"{__name__}.get_item_for_customer()")
def get_items_by_customer(
    db: Session, customer_id: int, skip: int = 0, limit: int = 100
):
    return (
        db.query(models.Item)
        .filter(models.Item.customer_id == customer_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


@tracer.wrap(name=f"{__name__}.create_customer_item()")
def create_customer_item(db: Session, item: schemas.ItemCreate, customer_id: int):
    db_item = models.Item(**item.dict(), customer_id=customer_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
