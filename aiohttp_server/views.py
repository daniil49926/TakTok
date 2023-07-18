from aiohttp import web


async def main_page(request):
    pool = request.app['DBPool']
    async with pool.acquire() as connection:
        async with connection.transaction():
            res = await connection.fetchval('select 2 ^ $1', 5)
            return web.Response(text=f"{res}")
