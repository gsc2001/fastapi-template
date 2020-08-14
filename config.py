# config here

import os

from dotenv import load_dotenv  # if using .env
from starlette.datastructures import Secret
# load local .env
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', None)

MAX_CONNECTIONS_COUNT = 10
MIN_CONNECTIONS_COUNT = 4

ALLOWED_HOSTS = [
    "*",
]

SECRET_KEY = str(Secret(os.getenv('SECRET_KEY', 'app_secret')))
