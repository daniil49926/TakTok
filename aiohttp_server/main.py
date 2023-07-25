import argparse

from aiohttp import web
from aiohttp_security import setup as setup_security
from aiohttp_security import SessionIdentityPolicy
from aiohttp_session import setup as setup_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from apps.profile.views import routes as routes_profile
from apps.takvideo.views import routes as routes_tak
from core.settings import settings
from core.security.db_auth import DBAuthorisationPolicy
from events import on_startup, on_shutdown


def init_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="TakTok")
    parser.add_argument("--host", help="Server host")
    parser.add_argument("--port", help="Server port")
    return parser.parse_args()


def run_server() -> None:
    args = init_args()
    app = web.Application()
    app.add_routes(routes_profile)
    app.add_routes(routes_tak)
    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_shutdown)
    setup_session(
        app=app,
        storage=EncryptedCookieStorage(
            secret_key=settings.SECRET_KEY_COOKIE_STORAGE
        )
    )
    setup_security(
        app=app,
        identity_policy=SessionIdentityPolicy(),
        autz_policy=DBAuthorisationPolicy()
    )
    web.run_app(
        app,
        host=args.host if args.host else settings.HOST,
        port=args.port if args.port else settings.PORT
    )


if __name__ == "__main__":
    run_server()
