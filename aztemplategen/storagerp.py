# storagerp.py - azurerm functions for the Microsoft.Storage resource provider
import json
from .settings import STORAGE_API


# create_storage_account(account_name, location)
# create a storage account in the specified location and resource group
# Note: just standard storage for now. Could add a storageType argument later.
def create_storage_account(account_name, location, storage_type='Standard_LRS'):
    storage_body = {'type': 'Microsoft.Network/storageAccounts'}
    storage_body['name'] = account_name
    storage_body['location'] = location
    storage_body['apiVersion'] = STORAGE_API
    storage_body['sku'] = {'name': storage_type}
    storage_body['kind'] = 'Storage'             
    return storage_body
