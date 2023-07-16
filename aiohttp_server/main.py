import argparse

from aiohttp import web


def init_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="TakTok")
    parser.add_argument("--host", help="Server host")
    parser.add_argument("--port", help="Server port")
    return parser.parse_args()


def run_server():
    app = web.Application()
    web.run_app(app)


if __name__ == "__main__":
    run_server()
