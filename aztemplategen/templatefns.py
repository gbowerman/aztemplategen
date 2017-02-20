# storagerp.py - azurerm functions for the Microsoft.Storage resource provider
import json

# new_temaplate()
# creates a new empty template disctionary
def new_template():
    template = {'$schema': 'http://schema.management.azure.com/schemas/2015-01-01/deploymentTemplate.json'}
    template['contentVersion'] = '1.0.0.0'
    template['resources'] = []
    return template

