from typing import Optional
import aiomcron

class AsyncRCONClient:
    """
    Talks to a minecraft instance over RCON
    """

    def __init__(self, host='127.0.0.1', rcon_port=25575, rcon_password=''):
        self._netloc = (host, rcon_port)
        self._rcon_client = aiomcron.Client(f"{host}:{rcon_port}", rcon_password)
    
    async def setup(self):
        return await self._rcon_client.setup()
    
    async def close(self):
        return await self._rcon_client.close()
    
    async def send_cmd(self, cmd: str) -> str:
        resp, code = await self._rcon_client.send_cmd(cmd)
        assert code == 0  # TODO: check if client will raise
        return resp
    
    async def send_cmd_and_extract(self, cmd: str, pattern: str) -> Optional[dict]:
        resp = await self.send_cmd(cmd)
        matches = re.match(pattern, resp)
        return matches.groupdict() if matches is not None else None
