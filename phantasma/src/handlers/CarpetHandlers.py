from aiohttp import web
import handlers.BaseHandler
import route.Route


class CarpetHandlers(handlers.BaseHandler.BaseHandler):
    def __init__(self, rcon_client):
        self._rcon_client = rcon_client
    
    def routes(self):
        return route.Route.RouteSet({
            '/mspt': {
                'get': {
                    'handler': self.mspt,
                    'perms': []
                }
            }
        })
    
    async def mspt(self):
        mspt = await self._rcon_client.mspt()
        return web.json_response({'mspt': mspt})