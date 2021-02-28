import os
import message
import config
import discord
import asyncio
# Help I've turned into a js dev
import aiostream

import server_status

client = discord.Client()
servers = None  # Initialized in init, love me some spaghetti

def init(config_path):
    global servers
    config.load_config(config_path)
    servers = {
        srv_info[0]: server_status.MCServerStatusUtil(name=srv_info[0], host=srv_info[1])
        for srv_info in config.config.get_servers()
    }

async def activity_messenger_task():
    global servers

    await client.wait_until_ready()
    print('Client is ready, activity task will begin running...')
    channel = client.get_channel(config.DISBOARD_CHANNEL_ID)

    event_sources = [server.watch() for server in servers.values()]
    async with aiostream.stream.merge(*event_sources).stream() as events:
        async for evt in events:
            if len(evt.events) == 0:
                continue

            msgs = message.build_evt_msgs(evt)
            for msg in msgs:
                if isinstance(msg, str):
                    await channel.send(msg)
                else:
                    # TODO: should flip conditionals
                    await channel.send(embed=msg)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(msg):
    global servers

    if msg.author == client.user:
        return

    if msg.content == "!source":
        await msg.channel.send("https://github.com/uint0/minecraft-stuff/tree/master/disboard")
    elif msg.content.startswith("!server"):
        cmd = msg.content.split(' ')
        try:
            server = msg.content.split(' ')[1]
            handle = servers[server.lower()]
            await msg.channel.send(embed=message.build_server_msg(
                handle.get_status()
            ))
        except (IndexError, KeyError):
            await msg.channel.send("!server <server name>")


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} <config file>', file=sys.stderr)
        sys.exit(1)

    init(sys.argv[1])
    client.loop.create_task(activity_messenger_task())
    client.run(config.DISBOARD_BOT_TOKEN)
