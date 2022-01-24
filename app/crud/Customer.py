from sqlalchemy.orm import Session
from ddtrace import tracer
import models
import schemas


@tracer.wrap(name=f"{__name__}.get_customer()")
def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()


@tracer.wrap(name=f"{__name__}.get_customer_by_email()")
def get_customer_by_email(db: Session, email: str):
    return db.query(models.Customer).filter(models.Customer.email == email).first()


@tracer.wrap(name=f"{__name__}.get_customers()")
def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Customer).offset(skip).limit(limit).all()


@tracer.wrap(name=f"{__name__}.create_customer()")
def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(email=customer.email)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer
