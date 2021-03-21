from aiohttp import web
from typing import List, Callable
import os.path
import util

class Route:
    def __init__(self, route: str, method: str, handler: Callable, permissions: List[str]):
        self._route = route
        self._method = method
        self._handler = handler
        self._permissions = permissions
    
    def as_aiohttp(self):
        method = getattr(web, self._method.lower())
        return method(self._route, self._handler)

class RouteSet:
    _routes: List[Route]

    def __init__(self, route_spec={}, /, prefix=''):
        self._routes = self._create_route_spec(route_spec, prefix)
    
    def _create_route_spec(self, route_spec, prefix):
        routes = []

        for route, methods in route_spec.items():
            for method, handler_spec in methods.items():
                routes.append(Route(
                    route=util.join_url([prefix, route]),
                    method=method,
                    handler=handler_spec['handler'],
                    permissions=handler_spec['perms'] if 'perms' in handler_spec else []
                ))

        return routes

    def mount_to_aiohttp(self, app: web.Application):
        app.add_routes([
            route.as_aiohttp()
            for route in self._routes
        ])

    def __add__(self, other):
        rs = RouteSet({})
        rs._routes = self._routes + other._routes
        return rs
