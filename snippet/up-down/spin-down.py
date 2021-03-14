"""
Spin minecraft server on a instance down - built for our usecase
"""

import common
import config
import mc_net

def get_n_online_players():
    status_ping = mc_net.StatusPing(host=config.TARGET_MC_SERVER)
    return status_ping.get_status()['players']['online']


def main():
    # 1. Check how many players are online
    n_online = get_n_online_players()

    # If there are online players, fail
    if n_online != 0:
        return fail()
    
    manager = common.InstanceManager(
        group_name=config.GROUP_NAME,
        vm_name=config.VM_NAME
    )
    manager.stop()
