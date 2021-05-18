#! /usr/local/bin/python3
import sys
import os
import requests
import json
import datetime
import urllib.parse
from load_json import LoadJson

# Load config 
config = LoadJson(sys.stdin)

# Gitlab API wants projectID urlencoded when using names
project_id = urllib.parse.quote(config.project,safe='')

# The filepath will be passed as argument
destination_path = sys.argv[1]

# Prepare GitlabRequest
params = ''
url = 'https://' + config.api_url + '/api/v4/projects/' + project_id + '/merge_requests/' + config.id + params
headers = {
  'Authorization': f'Bearer {config.access_token}'
}
payload={}

response = requests.request("GET", url, headers=headers, data=payload)

if response.status_code != 200 :
  print(f'StatusCode: {response.status_code}')
  print(f'Response: {response.content}')
  raise  Exception(f'Gitlab server returned error')  

json_response = response.json()

destination = os.path.join(destination_path, 'merge_list.json')

with open(destination,'w') as file:
    json.dump(response.json(), file, indent=4)

# F
concourse_response = {
  "version": config.version,
  "metadata": [
    { "name": "title", "value": config.title },
    { "name": "source_branch", "value": config.source_branch }
  ]
}

print(concourse_response)