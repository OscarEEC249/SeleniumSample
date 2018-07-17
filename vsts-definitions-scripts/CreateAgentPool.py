from requests.auth import HTTPBasicAuth
import urllib.parse
import pprint
import requests
import sys
import json

# Script parameters
vsts_intance = sys.argv[1]
agentpool_name = sys.argv[2]
vsts_token = sys.argv[3]

# URL information
vsts_url = vsts_intance + "/"
request_information = '_apis/distributedtask/pools?'
api_version = '4.1-preview.1'

# Request information
headers = {'Content-Type': 'application/json'}
credentials = HTTPBasicAuth('', vsts_token)

# New Agent Pool information
new_agentpool = {
    "name" : agentpool_name,
    "autoProvision" : "true"
}

# Convert body information to json
new_agentpool = json.dumps(new_agentpool)

# Endpoint creation
response = requests.post(vsts_url + request_information + 'api-version=' + api_version, auth=credentials, headers=headers, data=new_agentpool).json()

# Write response
pprint.pprint(response)