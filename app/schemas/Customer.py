from typing import List
from pydantic import BaseModel
from .Item import Item


class CustomerBase(BaseModel):
    email: str


class CustomerCreate(CustomerBase):
    pass


class Customer(CustomerBase):
    id: int
    items: List[Item] = []

    class Config:
        orm_mode = True
