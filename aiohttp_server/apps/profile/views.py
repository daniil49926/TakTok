from aiohttp import web

routes = web.RouteTableDef()


@routes.get('/profile/')
async def profile(request):
    return web.json_response({'profile ok?': 'ok'})
