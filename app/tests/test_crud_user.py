from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
import unittest
import crud
import schemas
import pytest


def test_create_user(client: TestClient, db: Session) -> None:
    email = "linh.do@yahoo.com"
    customer = schemas.CustomerCreate(email=email)
    user = crud.create_customer(db, customer=customer)
    assert user.email == email
    assert user.id == 1


def test_create_user_ensure_session_erased(client: TestClient, db: Session) -> None:
    email = "linh.do@yahoo.com"
    customer = schemas.CustomerCreate(email=email)
    user = crud.create_customer(db, customer=customer)
    assert user.email == email
    assert user.id == 1
