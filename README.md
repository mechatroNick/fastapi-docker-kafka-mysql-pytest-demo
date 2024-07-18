# TEMPLATE FastAPI + Kafka + MySQL + Consumer Healthcheck

## 1. FastAPI

### 1.1. New Model

Model folder structures:

```
.
├── Customer.py
├── Item.py
└── __init__.py
```

Example Model:

```python
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from repository.db import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    description = Column(String(50), index=False)
    title = Column(String(50), index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), index=True)

    customer = relationship("Customer", back_populates="items")
```

Guideline:

- Add the actual SQLAlchemy table definition + table relationship
- The type of each Model class is `sqlalchemy.ext.declarative.declarative_base`
- Each file is each table
- Table presents type of objects so plural is needed for table name `table="customers"`, but for file name use singular `Customer.py`
- Once done, import into the `__init__.py` file for ease of import later on `import models` will include both `Customer` and `Item`

```python
from .Customer import Customer
from .Item import Item
```

### 1.2. New Schema

Schema vs. Model:

- Schema is not the same as Model, and also does not have the same purpose
- Model represent the format of the data at the persistence level, ie. the Database
- Schema on the other hand is Data Class with schema enforcement and type checking capability
- Imagine having Schema as the object types for the Input and Output of each API
- Then when persisting or recalling data at the database level, you refer to the Models
- In and out -> Schema, Persistence -> Model

Schema folder structure:

```python
.
├── Customer.py
├── Item.py
└── __init__.py
```

Example Schema:

```python
from typing import Optional
from pydantic import BaseModel

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    customer_id: int

    class Config:
        orm_mode = True
```

Guideline:

- Type of schema is Pydantic.BaseModel
- Pydantic library has a lot of native data types for schema enforment, as well as standard decorator to check your entire object information validity
- Previously, `models/Item.py` was already defined and as the result SQLAlchemy will manage table `items` for you
- `ItemCreate` is the schema format for when you call an API to create an Item via PUT/POST API
- `Item` is the schema format for when you return the information of an Item to the client calling the GET API
- If there are DELETE API then there should be a `ItemDelete` schema, as well as a DELETE API
- Likewise if an item is to be alter, there should be a `ItemAlter` schema, as well as a PUT API that allow for editing an existing item
- Once done, import into the `__init__.py` file for ease of import later on `import schemas` will include both `Customer` and `Item`

```python
from .Item import ItemBase, ItemCreate, Item
from .Customer import CustomerBase, CustomerCreate, Customer
```
