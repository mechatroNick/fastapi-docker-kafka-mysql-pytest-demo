from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from typing import List

import schemas
import crud
from repository.db import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
