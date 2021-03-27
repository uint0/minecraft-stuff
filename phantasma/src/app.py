from aiohttp import web
import handlers.MinecraftHandlers, handlers.MetaHandlers
import route.Route

app = web.Application()

routes = route.Route.RouteSet()

mc_handler = handlers.MinecraftHandlers.MinecraftHandlers(None)
meta_handler = handlers.MetaHandlers.MetaHandlers(None)

routes += mc_handler.routes()
routes += meta_handler.routes()

routes.mount_to_aiohttp(app)

if __name__ == '__main__':
    web.run_app(app)
    