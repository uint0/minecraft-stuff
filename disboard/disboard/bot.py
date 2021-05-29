import asyncio

import discord
import discord.ext.commands

import cogs.server.command
import config


bot = discord.ext.commands.Bot(command_prefix='!')
bot.add_cog(cogs.server.command.ServerCommand(bot))


if __name__ ==  "__main__":
    import sys
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} <config dir>', file=sys.stderr)
        sys.exit(1)
    
    bot.run(config.discord.DISCORD_BOT_TOKEN)