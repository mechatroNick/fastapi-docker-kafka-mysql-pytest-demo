from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from repository.db import Base
from utils.decorators import (
    add_json_exporter_to_sqlalchemy_model,
    add_json_str_exporter_to_sqlalchemy_model,
)


@add_json_exporter_to_sqlalchemy_model
@add_json_str_exporter_to_sqlalchemy_model
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    description = Column(String(50), index=False)
    title = Column(String(50), index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), index=True)

    customer = relationship("Customer", back_populates="items")
