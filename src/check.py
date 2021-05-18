#! /usr/local/bin/python3
import sys
import requests
import json
from datetime import datetime
import urllib.parse
from load_json import LoadJson

# Load config 
config = LoadJson(sys.stdin)

# Gitlab API wants projectID urlencoded when using names
project_id = urllib.parse.quote(config.project,safe='')

# Only merged request of the present day are returned
current_day = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0).isoformat()

# Prepare GitlabRequest
params = ('?' + 
          'scope=all' + 
          '&state=merged' +
          f'&target_branch={config.source_branch}'
          f'&updated_after={current_day}'
          )
url = 'https://' + config.api_url + '/api/v4/projects/' + project_id + '/merge_requests' + params
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

# Create a new object with only relevant info about merge request
wanted_keys=['iid','title','project_id','source_branch']
check_response = []

for merge_request in json_response:
  simple_merge={}
  for key,value in merge_request.items():
    if key in wanted_keys:
      simple_merge[key] = value
  check_response.append(simple_merge)

print(check_response)
