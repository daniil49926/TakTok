import argparse

from aiohttp import web
from core.settings import settings
from routes import setup_routes


def init_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="TakTok")
    parser.add_argument("--host", help="Server host")
    parser.add_argument("--port", help="Server port")
    return parser.parse_args()


def run_server():
    args = init_args()
    app = web.Application()
    setup_routes(app)
    web.run_app(
        app,
        host=args.host if args.host else settings.HOST,
        port=args.port if args.port else settings.PORT
    )


if __name__ == "__main__":
    run_server()
