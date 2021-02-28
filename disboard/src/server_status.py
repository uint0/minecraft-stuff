# This really needs a more creative name

import typing
import asyncio
import mc_net
import util
from collections import namedtuple

MCServerStatus = namedtuple('MCServerStatus', ['name', 'players', 'occupation', 'motd', 'version', 'mod'])
MCServerStatusEvent = namedtuple('MCServerStatusEvent', ['event', 'info'])
MCServerStatusWatched = namedtuple('MCServerStatusWatched', ['status', 'events'])

class MCServerStatusUtil:
    EVENT_PLAYER_ACTIVITY = 1

    def __init__(self, /, name: str, host: str, port: int = 25565, timeout: int = 5):
        self._name = name
        self._net = (host, port)
        self._status_ping = mc_net.StatusPing(host=host, port=port, timeout=timeout)
    
    def get_raw_status(self):
        return self._status_ping.get_status()
    
    def get_status(self) -> MCServerStatus:
        status = self.get_raw_status()
        
        player_name_list = [player['name'] for player in status['players']['sample']] if status['players']['online'] > 0 else []

        return MCServerStatus(
            name=self._name,
            players=player_name_list,
            occupation=(status['players']['online'], status['players']['max']),
            motd=status['description']['text'],
            version=status['version']['name'],
            mod='forge' if 'forgeData' in status else 'vanilla'  # TODO: more mod type support
        )
    
    async def watch(self, poll_interval=5) -> typing.AsyncGenerator[MCServerStatusWatched, None]:
        prev_status = None
        while True:
            cur_status = self.get_status()

            if not prev_status:
                prev_status = cur_status
                continue

            player_diff = util.diff(prev_status.players, cur_status.players)
            events = []
            if player_diff is not None:
                events.append(MCServerStatusEvent(event=self.EVENT_PLAYER_ACTIVITY, info={'login': player_diff[0], 'logout': player_diff[1]}))
            
            yield MCServerStatusWatched(status=cur_status, events=events)
            
            prev_status = cur_status

            await asyncio.sleep(poll_interval)
