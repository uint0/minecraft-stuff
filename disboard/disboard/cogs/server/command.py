import discord
import discord.ext.commands as commands

import cogs.server.converter as converter
import cogs.util.decorators as deco
import config


NO_SUCH_SERVER_MSG = f"""
No such server. Find available servers with !server list
""".strip()


def get_status_color(status_code):
    if status_code == "PowerState/deallocated":
        return 0xff0000
    elif status_code == "PowerState/running":
        return 0x00ff00
    return 0x4f545c


class ServerCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @deco.require_channel(config.discord.DISCORD_CHANNEL_AZURE)
    async def server(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f"Usage: !server <status|start|stop|metrics|list|help> [server_name]")

    @server.command()
    @deco.require_channel(config.discord.DISCORD_CHANNEL_AZURE)
    async def status(self, ctx, server: converter.ServerConverter):
        if not server:
            return await ctx.send(NO_SUCH_SERVER_MSG)
        
        status = server.get_status()
        embed = discord.Embed(
            title=server.name,
            description=f"{server.resource_names.name}/{server.resource_names.group}",
            color=get_status_color(status.status_code)
        )
        embed.set_author(name="Azure Compute")
        embed.set_thumbnail(url="https://symbols.getvecta.com/stencil_27/102_vm-symbol.3da37253c9.png")

        embed.add_field(name="Status",      value=status.status_name,                        inline=True)
        embed.add_field(name="Status Time", value=str(status.status_time).rsplit('.', 1)[0], inline=True)
        embed.add_field(name="Game",        value=server.meta.get('game'),                   inline=True)
        embed.add_field(name="Owner",       value=', '.join(server.meta.get('owner')),       inline=True)
    
        embed.set_footer(text=f"!server status {server.called_name}")
        
        await ctx.send(embed=embed)


    @server.command()
    @deco.require_channel(config.discord.DISCORD_CHANNEL_AZURE)
    async def start(self, ctx, server: converter.ServerConverter):
        if not server:
            return await ctx.send(NO_SUCH_SERVER_MSG)
        
        await ctx.send("Not Implemented Yet D:")

    @server.command()
    @deco.require_channel(config.discord.DISCORD_CHANNEL_AZURE)
    async def stop(self, ctx, server: converter.ServerConverter):
        if not server:
            return await ctx.send(NO_SUCH_SERVER_MSG)
        
        await ctx.send("Not Implemented Yet D:")

    @server.command()
    @deco.require_channel(config.discord.DISCORD_CHANNEL_AZURE)
    async def metrics(self, ctx, server: converter.ServerConverter):
        if not server:
            return await ctx.send(NO_SUCH_SERVER_MSG)

        await ctx.send("Not Implemented Yet D:")
    
    @server.command(name='list')
    @deco.require_channel(config.discord.DISCORD_CHANNEL_AZURE)
    async def _list(self, ctx):
        await ctx.send(f"Available Servers: {', '.join(config.server.list_servers())}")

    @server.command()
    @deco.require_channel(config.discord.DISCORD_CHANNEL_AZURE)
    async def help(self, ctx):
        await ctx.send(f"Usage: !server <status|start|stop|metrics|list|help> [server_name]")