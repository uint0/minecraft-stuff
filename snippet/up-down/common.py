import config
import azure.identity
import azure.mgmt.compute

def get_credentials():
    subscription_id = config.AZURE_SUBSCRIPTION_ID
    credentials = azure.identity.DefaultAzureCredential()
    return credentials, subscription_id

class InstanceManager:
    def __init__(self, group_name, vm_name):
        self._group_name = group_name
        self._vm_name    = vm_name

        creds, subscription_id = get_credentials()
        self._client = azure.mgmt.compute.ComputeManagementClient(creds, subscription_id)

    def start(self):
        return self._client.virtual_machines.begin_start(
            self._group_name,
            self._vm_name
        )
    
    def stop(self):
        return self._client.virtual_machines.begin_power_off(
            self._group_name,
            self._vm_name
        )
    
    @staticmethod
    def wait(self, waiter):
        return waiter.wait()
