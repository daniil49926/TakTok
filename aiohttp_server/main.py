import argparse

from aiohttp import web
from apps.profile.views import routes as routes_profile
from apps.takvideo.views import routes as routes_tak
from core.settings import settings
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
    web.run_app(
        app,
        host=args.host if args.host else settings.HOST,
        port=args.port if args.port else settings.PORT
    )


if __name__ == "__main__":
    run_server()
