from aiohttp import web
import abc
import route.Route

class BaseHandler(abc.ABC):
    @abc.abstractmethod
    def routes(self) -> route.Route.RouteSet:
        pass

