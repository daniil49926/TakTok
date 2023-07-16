from aiohttp import web


async def main_page(request):
    return web.Response(text="Development is in progress, pls wait")
