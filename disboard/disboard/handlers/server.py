from collections import namedtuple
import datetime as dt

import azure.identity
import azure.mgmt.compute

import config


ServerStatus = namedtuple('ServerStatus', ['status_code', 'status_name', 'status_time'])
ServerNames  = namedtuple('ServerNames', ['name', 'group'])


def get_credentials():
    subscription_id = config.azure.AZURE_SUBSCRIPTION_ID
    credentials = azure.identity.DefaultAzureCredential()
    return credentials, subscription_id


class ServerManager:
    def __init__(self, vm_name, group_name):
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
        return self._client.virtual_machines.begin_deallocate(
            self._group_name,
            self._vm_name
        )
    
    def get_vm_instance_view(self):
        return self._client.virtual_machines.instance_view(
            self._group_name,
            self._vm_name
        )
    

    @staticmethod
    def wait(self, waiter):
        return waiter.wait()


class ServerForbiddenException(Exception):
    """ Raised when no the requester does not have perms """

class ServerNotConfiguredException(Exception):
    """ Raised when a server cannot be found in config """

def requires_perm(perm):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            if perm not in self._perms:
                raise ServerForbiddenException(f"Required perm {perm} was not in found in allowed perms for this server")
            return func(self, *args, **kwargs)
        return wrapper
    return decorator


class Server:
    def __init__(self, vm_name):
        server_info = config.server.get_server(vm_name)
        if server_info is None:
            raise ServerNotConfiguredException(f"Could not find {vm_name} or alias")

        self._called_name = vm_name
        self._server_info = server_info
        self._resource    = server_info['resource']
        self._meta        = server_info['meta']
        self._perms       = set(server_info['perms'])

        self._manager = ServerManager(self._resource['name'], self._resource['group'])
    
    @property
    def resource_names(self):
        return ServerNames(
            name=self._resource['name'],
            group=self._resource['group']
        )
    
    @property
    def meta(self):
        return self._meta.copy()
    
    @property
    def name(self):
        return self._server_info['name']
    
    @property
    def called_name(self):
        return self._called_name


    @requires_perm('read')
    def get_status(self):
        instance_view = self._manager.get_vm_instance_view()
        statuses = instance_view.statuses
        provision_status = statuses[0]
        power_status = statuses[1]

        return ServerStatus(
            status_code=power_status.code,
            status_name=power_status.display_status,
            status_time=dt.datetime.now(dt.timezone.utc) - provision_status.time
        )
    
    @requires_perm('power')
    def start(self):
        return self._manager.start()
    
    @requires_perm('stop')
    def stop(self):
        return self._manager.stop()
