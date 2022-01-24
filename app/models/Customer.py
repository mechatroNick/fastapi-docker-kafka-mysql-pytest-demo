from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from repository.db import Base
from utils.decorators import (
    add_json_exporter_to_sqlalchemy_model,
    add_json_str_exporter_to_sqlalchemy_model,
)


@add_json_exporter_to_sqlalchemy_model
@add_json_str_exporter_to_sqlalchemy_model
class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    email = Column(String(50), unique=True, index=True)

    items = relationship("Item", back_populates="customer")
