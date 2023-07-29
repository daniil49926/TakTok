import aiohttp_jinja2
from aiohttp import web
from aiohttp_security import authorized_userid

from apps.profile.utils import get_user_by_name
from apps.takvideo.utils import get_videos
from core.utils.redirect import redirect
from core.settings import settings

routes = web.RouteTableDef()


@routes.get('/tak/', name='tak')
@aiohttp_jinja2.template('tak.html')
async def tak(request):
    is_authorised_user = await authorized_userid(request)
    if not is_authorised_user:
        raise redirect(request.app.router, 'login')

    async with settings.PG_POOL.acquire() as conn:
        current_user = await get_user_by_name(conn, is_authorised_user)
        videos = await get_videos(conn)

    return {"user": current_user, 'videos': videos}
