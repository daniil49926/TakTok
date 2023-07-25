from aiohttp import web


def redirect(router, route_name):
    return web.HTTPFound(router[route_name].url_for())
