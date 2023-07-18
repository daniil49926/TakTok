import asyncpg

from core.settings import settings
from aiohttp.web import Application


async def on_startup(app: Application) -> None:
    app['DBPool'] = await asyncpg.create_pool(dsn=settings.PG_DSN)


async def on_shutdown(app: Application) -> None:
    app['DBPool'].close()
