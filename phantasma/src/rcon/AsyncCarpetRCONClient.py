import re

from rcon.AsyncRCONClient import AsyncRCONClient

# TODO: return model
class AsyncCarpetRCONClient(AsyncRCONClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    async def list_(self):
        matches = await self.send_cmd_and_extract(
            'list',
            r'^There are (?P<n_online>\d+) of a max of (?P<max_supported>\d+) players online: (?P<player_list>.*)$'
        )

        matches['player_list'] = [p.strip() for p in matches['player_list'].split(',')]
        return matches

    async def mspt(self):
        resp = await self.send_cmd('mspt')
        if resp.startswith('Unknown or incomplete command'):
            # TODO: raise unimplemented?
            return None
        
        return {'mspt': float(resp)}