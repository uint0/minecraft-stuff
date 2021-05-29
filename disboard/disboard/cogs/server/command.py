import functools

import discord
import discord.ext.commands as commands

import cogs.server.converter as converter
import config



NO_SUCH_SERVER_MSG = f"""
No such server. Find available servers with !server list
""".strip()


def require_channel(channel):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(self, ctx, *args, **kwargs):
            if str(ctx.channel.id) != str(channel):
                return None
            return await func(self, ctx, *args, **kwargs)
        return wrapper
    return decorator


class ServerCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @require_channel(config.discord.DISCORD_CHANNEL_AZURE)
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

        embed.add_field(name="Status",      value=status.status_name,                  inline=True)
        embed.add_field(name="Status Time", value=status.uptime,                       inline=True)
        embed.add_field(name="Game",        value=server.meta.get('game'),             inline=True)
        embed.add_field(name="Owner",       value=', '.join(server.meta.get('owner')), inline=True)
    
        embed.set_footer(text=f"!server status {server.called_name}")
        
        await ctx.send(embed)


    @commands.command()
    @require_channel(config.discord.DISCORD_CHANNEL_AZURE)
    async def start(self, ctx, server: converter.ServerConverter):
        if not server:
            return await ctx.send(NO_SUCH_SERVER_MSG)
        
        await ctx.send("Not Implemented Yet D:")

    @commands.command()
    @require_channel(config.discord.DISCORD_CHANNEL_AZURE)
    async def stop(self, ctx, server: converter.ServerConverter):
        if not server:
            return await ctx.send(NO_SUCH_SERVER_MSG)
        
        await ctx.send("Not Implemented Yet D:")

    @commands.command()
    @require_channel(config.discord.DISCORD_CHANNEL_AZURE)
    async def metrics(self, ctx, server: converter.ServerConverter):
        if not server:
            return await ctx.send(NO_SUCH_SERVER_MSG)

        await ctx.send("Not Implemented Yet D:")
    
    @commands.command(name='list')
    @require_channel(config.discord.DISCORD_CHANNEL_AZURE)
    async def _list(self, ctx):
        await ctx.send(f"Available Servers: {', '.join(config.server.list_servers())}")

    @commands.command()
    @require_channel(config.discord.DISCORD_CHANNEL_AZURE)
    async def help_cmd(self, ctx):
        await ctx.send(f"Usage: !server <status|start|stop|metrics|list|help> [server_name]")