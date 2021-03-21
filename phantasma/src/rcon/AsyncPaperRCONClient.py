import rcon.AsyncRCONClient

class AsyncPaperRCONClient(rcon.AsyncRCONClient.AsyncRCONClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def list_(self):
        resp = self.send_cmd('list')
        return []
