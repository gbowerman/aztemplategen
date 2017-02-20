# networkrp.py - azurerm functions for the Microsoft.Network resource provider
import json
from .settings import NETWORK_API


# create_lb_with_nat_pool(lb_name, public_ip_name, fe_start_port, fe_end_port, backend_port, location)
# create a load balancer with inbound NAT pools
def create_lb_with_nat_pool(lb_name, public_ip_name, fe_start_port, fe_end_port, backend_port, \
    location):
    lb_body = {'type': 'Microsoft.Network/loadBalancers'}
    lb_body['name'] = lb_name
    lb_body['location'] = location
    lb_body['apiVersion'] = NETWORK_API

    # handle dependsOn
    lb_body['dependsOn'] = ['Microsoft.Network/publicIPAddresses/' + public_ip_name]
    
    frontendipcconfig = {'name': 'LoadBalancerFrontEnd'}
    public_ip_id = "[resourceId('Microsoft.Network/publicIPAddresses','" + pip_name + "')]"
    fipc_properties = {'publicIPAddress': {'id': public_ip_id}}
    frontendipcconfig['properties'] = fipc_properties
    properties = {'frontendIPConfigurations': [frontendipcconfig]}
    properties['backendAddressPools'] = [{'name': 'bepool'}]
    inbound_natpool = {'name': 'natpool'}
    lbfe_id = "[concat(resourceId('Microsoft.Network/loadBalancers','" + lb_name + \
        "'), '/frontendIPConfigurations/LoadBalancerFrontEnd')]"
    ibnp_properties = {'frontendIPConfiguration': {'id': lbfe_id}}
    ibnp_properties['protocol'] = 'tcp'
    ibnp_properties['frontendPortRangeStart'] = fe_start_port
    ibnp_properties['frontendPortRangeEnd'] = fe_end_port
    ibnp_properties['backendPort'] = backend_port
    inbound_natpool['properties'] = ibnp_properties
    properties['inboundNatPools'] = [inbound_natpool]
    lb_body['properties'] = properties
    return lb_body


# create_nic(nic_name, public_ip_name, subnet_id, location)
# create a network interface with an associated public ip address
def create_nic(nic_name, public_ip_name, vnet_name, location, nsg_id=None):
    nic_body = {'type': 'Microsoft.Network/networkInterfaces'}
    nic_body['name'] = nic_name
    nic_body['location'] = location
    nic_body['apiVersion'] = NETWORK_API
    
    # handle dependsOn
    nic_body['dependsOn'] = ['Microsoft.Network/publicIPAddresses/' + public_ip_name]

    ipconfig = {'name': 'ipconfig1'}
    ipc_properties = {'privateIPAllocationMethod': 'Dynamic'}
    public_ip_id = "[resourceId('Microsoft.Network/publicIPAddresses','" + public_ip_name + "')]"
    ipc_properties['publicIPAddress'] = {'id': public_ip_id}
    subnet_id = "[concat(resourceId('Microsoft.Network/virtualNetworks','" + vnet_name + "'), '/subnets/subnet')]"
    ipc_properties['subnet'] = {'id': subnet_id}
    ipconfig['properties'] = ipc_properties
    properties = {'ipConfigurations': [ipconfig]}
    if nsg_id is not None:
        properties['networkSecurityGroup'] = {'id': nsg_id}
    nic_body['properties'] = properties
    return nic_body

	
# create_nsg(access_token, subscription_id, resource_group, nsg_name, location)
# create network security group (use create_nsg_rule() to add rules to it)
def create_nsg(nsg_name, location):
    nsg_body = {'type': 'Microsoft.Network/networkSecurityGroups'}
    nsg_body['name'] = nsg_name
    nsg_body['location'] = location
    nsg_body['apiVersion'] = NETWORK_API 
    return nsg_body


# create_nsg_rule(nsg_name, nsg_rule_name, description, protocol='Tcp', source_range='*', \
# destination_range='*', source_prefix='Internet', destination_prefix='*', access = 'Allow', \
# priority=100, direction='Inbound')
# create network security group rule
def create_nsg_rule(nsg_name, nsg_rule_name, description, protocol='Tcp', source_range='*', \
    destination_range='*', source_prefix='Internet', destination_prefix='*', access = 'Allow', \
    priority=100, direction='Inbound'):
    nsg_body = {'name': nsg_rule_name}
    properties = {'description': description}
    properties['protocol'] = protocol
    properties['sourcePortRange'] = source_range
    properties['destinationPortRange'] = destination_range
    properties['sourceAddressPrefix'] = source_prefix
    properties['destinationAddressPrefix'] = destination_prefix
    properties['sourceAddressPrefix'] = '*'
    properties['destinationAddressPrefix'] = '*'
    properties['access'] = access
    properties['priority'] = priority
    properties['direction'] = direction
    nsg_body = {'properties': properties}
    return nsg_body


# create_public_ip(public_ip_name, dns_label, location)
# create a public ip address
def create_public_ip(public_ip_name, dns_label, location):
    ip_body = {'type': 'Microsoft.Network/publicIPAddresses'}
    ip_body['name'] = public_ip_name
    ip_body['location'] = location
    ip_body['apiVersion'] = NETWORK_API 
    properties = {'publicIPAllocationMethod': 'Dynamic'}
    properties['dnsSettings'] = {'domainNameLabel': dns_label}
    ip_body['properties'] = properties
    return ip_body


# create_vnet( name, location, address_prefix='10.0.0.0/16', subnet_prefix='10.0.0.0/16', \
#  nsg_id=None))
# create a VNet with specified name and location. Optional subnet address prefix.
def create_vnet(name, location, address_prefix='10.0.0.0/16', subnet_prefix='10.0.0.0/16', \
    nsg_id=None):
    vnet_body = {'type': 'Microsoft.Network/virtualNetworks'}
    vnet_body['name'] = name
    vnet_body['location'] = location
    vnet_body['apiVersion'] = NETWORK_API 
    properties = {'addressSpace': {'addressPrefixes': [address_prefix]}}
    subnet = {'name': 'subnet'}
    subnet['properties'] = {'addressPrefix': subnet_prefix}
    if nsg_id is not None:
        subnet['properties']['networkSecurityGroup'] = {'id': nsg_id}
    properties['subnets'] = [subnet]
    vnet_body['properties'] = properties
    return vnet_body

