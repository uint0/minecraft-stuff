from aiohttp import web
import route.Route

class MinecraftHandlers:
    def __init__(self, rcon_client):
        self._rcon_client = rcon_client
    
    def routes(self):
        return route.Route.RouteSet({
            '/whitelist': {
                'get': {
                    'handler': self.whitelist_get,
                    'perms': []
                },
                'put': {
                    'handler': self.whitelist_put,
                    'perms': []
                },
                'delete': {
                    'handler': self.whitelist_delete,
                    'perms': []
                }
            },
            '/list': {
                'get': {
                    'handler': self.list_online,
                    'perms': []
                }
            }
        }, prefix='/minecraft')
    
    async def list_online(self, request):
        return web.json_response({'path': 'list'})
    
    async def whitelist_get(self, request):
        return web.json_response({'path': 'wlget'})

    async def whitelist_put(self, request):
        return web.json_response({'path': 'put'})

    async def whitelist_delete(self, request):
        return web.json_response({'path': 'delete'})