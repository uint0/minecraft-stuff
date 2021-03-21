from aiohttp import web
import abc

class BaseHandler(abc.ABC):
    @abc.abstractmethod
    def routes(self):
        pass

