import os
import json

# ENVIRON
DISBOARD_CHANNEL_ID = int(os.environ['DISBOARD_CHANNEL_ID'])
DISBOARD_BOT_TOKEN = os.environ['DISCORD_BOT_TOKEN']

# CONFIG FILE
class Config:
    def __init__(self, path):
        self._config = json.load(open(path))
    
    def get_servers(self):
        return [
            (server_name, server_info['host'])
            for server_name, server_info in self._config['servers'].items()
        ]
    
    def get_server_icon(self, server):
        try:
            return self._config['servers'][server]['icon']
        except KeyError:
            return None
    
    def get_flavor(self, server, event):
        try:
            return self._config['servers'][server]['flavor'][event]
        except KeyError:
            return None
        

config = None

# Imagine doing this properly
def load_config(path):
    global config
    config = Config(path)