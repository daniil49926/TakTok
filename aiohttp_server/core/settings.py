import os

from dataclasses import dataclass
from asyncpg import Pool
from core.utils.load_env import load_environ

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

load_environ(_BASE_DIR)


@dataclass
class __Settings:
    HOST: str = os.environ.get("APPLICATION_HOST")
    PORT: int = os.environ.get("APPLICATION_PORT")

    RELOAD: bool = True

    PG_USER: str = os.environ.get('PG_USER')
    PG_PASS: str = os.environ.get('PG_PASS')
    PG_HOST: str = os.environ.get('PG_HOST')
    PG_PORT: int = os.environ.get('PG_PORT')
    PG_DB: str = os.environ.get('PG_DB')

    PG_DSN: str = f"postgres://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB}"

    PG_POOL: Pool = None

    SECRET_KEY_COOKIE_STORAGE: bytes = b'Thirty  two  length  bytes  key.'


settings = __Settings()
