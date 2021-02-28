import discord
import server_status
import config

def get_server_icon(server):
    return config.config.get_server_icon(server)

def login_embed(server, player, action):
    if action == "login":
        descriptor = "joined"
        color = 0x00ff00
        footer = config.config.get_flavor(server, action)
    elif action == "logout":
        descriptor = "left"
        color = 0xff0000
        footer = config.config.get_flavor(server, action)

    embed = discord.Embed(title=f"{player} {descriptor} the game", color=color)
    embed.set_author(name=server.title(), icon_url=get_server_icon(server))
    embed.set_footer(text=footer)

    return embed

def build_evt_msgs(evt):
    # For now just single handle login events
    if len(evt.events) == 0: return []

    msgs = []
    event = evt.events[0]

    if event.event == server_status.MCServerStatusUtil.EVENT_PLAYER_ACTIVITY:
        for player in event.info['login']:
            msgs.append(login_embed(evt.status.name, player, 'login'))
        for player in event.info['logout']:
            msgs.append(login_embed(evt.status.name, player, 'logout'))

    return msgs

def build_server_msg(status):
    embed = discord.Embed(
        title=status.name.title(),
        description=f"{status.occupation[0]}/{status.occupation[1]} Players",
        color=0xffe21a
    )

    embed.set_thumbnail(url=get_server_icon(status.name))

    player_list = ", ".join(status.players) if len(status.players) > 0 else "None"
    embed.add_field(name="Online", value=player_list)

    return embed
