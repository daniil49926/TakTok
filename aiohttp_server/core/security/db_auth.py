from aiohttp_security.abc import AbstractAuthorizationPolicy
from core.settings import settings


class DBAuthorisationPolicy(AbstractAuthorizationPolicy):
    _sql_get_user_by_username = """
        SELECT 1 FROM public."Profile" pr 
            WHERE pr.username = $1
    """ # noqa

    async def authorized_userid(self, identity):
        async with settings.PG_POOL.acquire() as coon:
            user = await coon.fetch(self._sql_get_user_by_username, identity)
        return identity if user else None

    async def permits(self, identity, permission, context=None):
        return True if identity else False
