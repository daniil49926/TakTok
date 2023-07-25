import asyncpg

from core.settings import settings
from aiohttp.web import Application


async def on_startup(_: Application) -> None:
    settings.PG_POOL = await asyncpg.create_pool(dsn=settings.PG_DSN)


async def on_shutdown(_: Application) -> None:
    await settings.PG_POOL.close()
