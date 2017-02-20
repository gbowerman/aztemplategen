import aztemplategen
from haikunator import Haikunator
import json

# set up some starting params
location = 'southcentralus'
vnet_name = 'aztvnet'
pip_name = 'aztpip'
dns_label = 'aztdns'
nic_name = 'aztnic'
vm_name = 'aztvmtest'
publisher = 'Canonical'
offer = 'UbuntuServer'
sku = '16.04-LTS'
vm_size = 'Standard_D1_V2'
version = 'latest'
password = Haikunator().haikunate(delimiter=',') # creates random password
print('Created new password = ' + password)

# create a new template dictionary
new_template = aztemplategen.new_template()

# create dictionaries for individual resources
vnet_def = aztemplategen.create_vnet(vnet_name, location)
ip_def = aztemplategen.create_public_ip(pip_name, dns_label, location)
nic_def = aztemplategen.create_nic(nic_name, pip_name, vnet_name, location)
vm_def = aztemplategen.create_vm(vm_name, vm_size, publisher, offer, sku, version, nic_name, \
    location, password=password)

# build template
new_template['resources'].append(vnet_def)
new_template['resources'].append(ip_def)
new_template['resources'].append(nic_def)
new_template['resources'].append(vm_def)

# print to stndard out
print(json.dumps(new_template, sort_keys=False, indent=2, separators=(',', ': ')))