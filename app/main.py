from typing import Optional, List
from fastapi import FastAPI
from ddtrace import tracer
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
import crud
from  consumers import start_consumers
from router.api import api_router
from repository.db import init_db
from utils.logger import configure_logging

init_db()
configure_logging()
start_consumers()

app = FastAPI()
app.include_router(api_router)
