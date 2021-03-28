from aiohttp import web
import handlers.BaseHandler
import route.Route


class MetaHandlers(handlers.BaseHandler.BaseHandler):
    def __init__(self, rcon_client, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._rcon_client = rcon_client
    
    def routes(self):
        return route.Route.RouteSet({
            '/info': {
                'get': {
                    'handler': self.version,
                    'perms': []
                }
            }
        }, prefix='/meta')
    
    async def info(self, request):
        return web.json_response({
            'server': {
                'version': '1.16.4',
                'server': 'fabric/carpet'
            },
            'phantasma': {
                'version': '0.0.1'
            }
        })
