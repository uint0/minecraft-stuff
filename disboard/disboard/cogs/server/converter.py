import discord.ext.commands as commands

import handlers.server

class ServerConverter(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            return handlers.server.Server(argument)
        except handlers.server.ServerNotConfiguredException:
            return None
