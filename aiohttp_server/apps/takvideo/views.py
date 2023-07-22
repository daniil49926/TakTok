from aiohttp import web

routes = web.RouteTableDef()


@routes.get('/tak/')
async def tak(request):
    return web.json_response({'tak ok?': 'ok'})
