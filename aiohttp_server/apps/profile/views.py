from aiohttp import web

routes = web.RouteTableDef()


@routes.get('/profile/login/', name='login')
async def login(request):
    return web.json_response({'profile ok?': 'ok'})
