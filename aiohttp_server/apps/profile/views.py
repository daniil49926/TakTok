import aiohttp_jinja2
from aiohttp import web
from aiohttp_security import authorized_userid, remember, forget

from apps.profile.forms import validate_login
from core.utils.redirect import redirect
from core.settings import settings

routes = web.RouteTableDef()


@routes.get('/profile/login/', name='login')
@aiohttp_jinja2.template('login.html')
async def login(request):
    is_authorised = await authorized_userid(request)
    if is_authorised:
        raise redirect(request.app.router, 'tak')
    return {}


@routes.post('/profile/login/', name='login_post')
@aiohttp_jinja2.template('login.html')
async def login(request):
    form = await request.post()
    async with settings.PG_POOL.acquire() as conn:
        error, user = await validate_login(conn, form)

        if error:
            return {'error': error}
        else:
            response = redirect(request.app.router, 'tak')

            await remember(request, response, user[3])

            raise response
    return {}


@routes.get('/profile/logout/', name='logout')
async def logout(request):
    response = redirect(request.app.router, 'login')
    await forget(request, response)
    return response
