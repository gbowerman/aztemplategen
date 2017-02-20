# computerp.py - azurerm functions for the Microsoft.Compute resource provider
from .settings import COMP_API, NETWORK_API
import json

# create_as(as_name, update_domains, fault_domains, location)
# create availability set
def create_as(as_name, update_domains, fault_domains, location):
    as_body = {'type': 'Microsoft.Compute/availabilitySets'}
    as_body['name'] = as_name
    as_body['location'] = location
    as_body['apiVersion'] = COMP_API
    properties = {'platformUpdateDomainCount': update_domains}
    properties['platformFaultDomainCount'] = fault_domains
    as_body['properties'] = properties
    return as_body


# create_vm(vm_name, vm_size, publisher, offer, sku, version, nic_name, location, \
#     storage_type='standard_LRS', username='azure', password=None, public_key=None)
# create a simple virtual machine - in most cases deploying an ARM template might be easier
def create_vm(vm_name, vm_size, publisher, offer, sku, version, nic_name, location, \
    storage_type='Standard_LRS', osdisk_name=None, username='azure', password=None, public_key=None):
    vm_body = {'type': 'Microsoft.Compute/virtualMachines'}
    vm_body['name'] = vm_name
    vm_body['location'] = location
    vm_body['apiVersion'] = COMP_API

    # handle dependsOn
    vm_body['dependsOn'] = ['Microsoft.Network/networkInterfaces/' + nic_name]

    properties = {'hardwareProfile': {'vmSize': vm_size}}
    image_reference = {'publisher': publisher, 'offer': offer, 'sku': sku, 'version': version}
    storage_profile = {'imageReference': image_reference}
    if osdisk_name is None:
        osdisk_name = vm_name + 'osdisk'
    os_disk = {'name': osdisk_name}
    os_disk['managedDisk'] = {'storageAccountType': storage_type}
    os_disk['caching'] = 'ReadWrite'
    os_disk['createOption'] = 'fromImage'
    storage_profile['osDisk'] = os_disk
    properties['storageProfile'] = storage_profile
    os_profile = {'computerName': vm_name}
    os_profile['adminUsername'] = username
    if password is not None:
        os_profile['adminPassword'] = password
    if public_key is not None:
        if password is None:
            disable_pswd = True
        else:
            disable_pswd = False
        linux_config = {'disablePasswordAuthentication': disable_pswd}
        pub_key = {'path': '/home/' + username +'/.ssh/authorized_keys'}
        pub_key['keyData'] = public_key
        linux_config['ssh'] = {'publicKeys': [pub_key]}
        os_profile['linuxConfiguration'] = linux_config
    properties['osProfile'] = os_profile
    nic_id = "[resourceId('Microsoft.Network/networkInterfaces','" + nic_name + "')]"
    network_profile = {'networkInterfaces': [{'id': nic_id, 'properties': {'primary': True}}]}
    properties['networkProfile'] = network_profile
    vm_body['properties'] = properties
    return vm_body


# create_vmss(vmss_name, vm_size, capacity, publisher, offer, sku, version, subnet_id, be_pool_id,\
#    lb_pool_id, location, storage_type='Standard_LRS', username='azure', password=None, \
#    public_key=None, overprovision='true', upgradePolicy='Manual')
# create virtual machine scale set
def create_vmss(vmss_name, vm_size, capacity, publisher, offer, sku, version, vnet_name, \
    be_pool_id, lb_pool_id, location, storage_type='Standard_LRS', username='azure', \
    password=None, public_key=None, overprovision='true', upgradePolicy='Manual'):
    vmss_body = {'type': 'Microsoft.Compute/virtualMachineScaleSets'}
    vmss_body['name'] = vm_name
    vmss_body['location'] = location
    vmss_body['apiVersion'] = COMP_API

    # handle dependsOn
    # vnet
    vm_body['dependsOn'] = ['Microsoft.Network/virtualNetworks/' + vnet_name]
    
    subnet_id = "[concat(resourceId('Microsoft.Network/virtualNetworks','" + vnet_name + "'),'/subnets/subnet')]"

    # load balancer
    if be_pool_id is not None:
        lbnameidx1 = subnet_id.rfind('loadBalancers/') + 14
        lbnameidx2 = subnet.rfind('/backendAddressPools')
        lb_name = subnet_id[vnetnameidx1:vnetnameidx2]
        vm_body['dependsOn'].append('Microsoft.Network/loadBalancers/' + lb_name)

    vmss_sku = {'name': vm_size, 'tier': 'Standard', 'capacity': capacity}
    vmss_body['sku'] = vmss_sku
    properties = {'overprovision': overprovision}
    properties['upgradePolicy'] = {'mode': upgradePolicy}
    os_profile = {'computerNamePrefix': vmss_name}
    os_profile['adminUsername'] = username
    if password is not None:
        os_profile['adminPassword'] = password
    if public_key is not None:
        if password is None:
            disable_pswd = True
        else:
            disable_pswd = False
        linux_config = {'disablePasswordAuthentication': disable_pswd}
        pub_key = {'path': '/home/' + username +'/.ssh/authorized_keys'}
        pub_key['keyData'] = public_key
        linux_config['ssh'] = {'publicKeys': [pub_key]}
        os_profile['linuxConfiguration'] = linux_config
    vm_profile = {'osProfile': os_profile}
    os_disk = {'createOption': 'fromImage'}
    os_disk['managedDisk'] = {'storageAccountType': storage_type}
    os_disk['caching'] = 'ReadWrite'
    storage_profile = {'osDisk': os_disk}
    storage_profile['imageReference'] = \
        {'publisher': publisher, 'offer': offer, 'sku': sku, 'version': version} 
    vm_profile['storageProfile'] = storage_profile
    nic = {'name': vmss_name}
    ip_config = {'name': vmss_name}
    ip_properties = {'subnet': { 'id': subnet_id}}
    if be_pool_id is not None:
        ip_properties['loadBalancerBackendAddressPools'] = [{'id': be_pool_id}]
    if lb_pool_id is not None:
        ip_properties['loadBalancerInboundNatPools'] = [{'id': lb_pool_id}]
    ip_config['properties'] = ip_properties
    nic['properties'] = {'primary': True, 'ipConfigurations': [ip_config]}
    network_profile = {'networkInterfaceConfigurations': [nic]}
    vm_profile['networkProfile'] = network_profile
    properties['virtualMachineProfile'] = vm_profile
    vmss_body['properties'] = properties
    return vmss_body
