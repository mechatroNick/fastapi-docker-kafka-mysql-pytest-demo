from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends, APIRouter
from typing import List


import schemas
import crud
from repository.db import get_db
import producers


router = APIRouter()


@router.post("/", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    db_customer = crud.get_customer_by_email(db, email=customer.email)
    if db_customer:
        raise HTTPException(status_code=400, detail="Email already registered")
    customer_model = crud.create_customer(db=db, customer=customer)
    producers.NotifyCustomerProducer.produce(customer_model.to_json_str())
    return customer_model


@router.get("/", response_model=List[schemas.Customer])
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    customers = crud.get_customers(db, skip=skip, limit=limit)
    return customers


@router.get("/{customer_id}", response_model=schemas.Customer)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud.get_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer


@router.post("/{customer_id}/items/", response_model=schemas.Item)
def create_item_for_customer(
    customer_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    item_model = crud.create_customer_item(db=db, item=item, customer_id=customer_id)
    producers.NotifyItemProducer.produce(item_model.to_json_str())
    return item_model


@router.get("/{customer_id}/items/", response_model=List[schemas.Item])
def read_item_for_customer(
    customer_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    db_customer = crud.get_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return crud.get_items_by_customer(
        db=db, customer_id=customer_id, skip=skip, limit=limit
    )
