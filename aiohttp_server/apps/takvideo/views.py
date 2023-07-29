from aiohttp import web
from aiohttp_security import authorized_userid

from core.utils.redirect import redirect

routes = web.RouteTableDef()


@routes.get('/tak/', name='tak')
async def tak(request):
    is_authorised = await authorized_userid(request)
    if not is_authorised:
        raise redirect(request.app.router, 'login')

    return 1
