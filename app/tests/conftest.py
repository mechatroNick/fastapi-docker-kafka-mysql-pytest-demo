from typing import Generator
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from repository.db import init_db, SessionLocal
from router.api import api_router
import models


@pytest.fixture(scope="session")
def app():
    init_db()
    app = FastAPI()
    app.include_router(api_router)
    return app


@pytest.fixture(scope="session")
def client(app) -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def db() -> Generator:
    db_session_ = SessionLocal()

    yield db_session_

    # Cleaning up before the next test execution
    db_session_.query(models.Customer).delete()
    db_session_.query(models.Item).delete()
    db_session_.commit()
    db_session_.close()