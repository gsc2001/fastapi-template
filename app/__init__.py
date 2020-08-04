from fastapi import FastAPI
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from .utils.db_loader import connect_db, disconnect_db
import config
from .utils.error_handlers import http_error_handler, http_422_error_handler
from .core import router as core_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# connect to db
app.add_event_handler("startup", connect_db)
app.add_event_handler('shutdown', disconnect_db)

app.add_exception_handler(HTTPException, http_error_handler)
app.add_exception_handler(
    HTTP_422_UNPROCESSABLE_ENTITY, http_422_error_handler)

# add routers
app.include_router(core_router, prefix="/core")
