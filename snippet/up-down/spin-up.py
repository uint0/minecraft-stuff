import common

def main():
    manager = common.InstanceManager(
        group_name=config.GROUP_NAME,
        vm_name=config.VM_NAME
    )
    manager.start()
