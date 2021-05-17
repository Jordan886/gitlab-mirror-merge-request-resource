#! /usr/bin/python3
import sys
import os
import requests
import json
from datetime import datetime
import urllib.parse
from pprint import pprint
from load_json import LoadJson

# Load config 
config = LoadJson(sys.stdin)

# Gitlab API wants projectID urlencoded when using names
project_id = urllib.parse.quote(config.project,safe='')

# The filepath will be passed as argument
source_path = sys.argv[1]

# Read the merge from the input step
source = os.path.join(source_path, 'merge_list.json')
with open(source) as file:
    merge_request = json.loads(file.read())


# Prepare GitlabRequest
params = ''
url = 'https://' + config.api_url + '/api/v4/projects/' + project_id + '/merge_requests/' + params
headers = {
  'Authorization': f'Bearer {config.access_token}'
}
payload={
  "source_branch": merge_request['source_branch'],
  "target_branch": config.target_branch,
  "title": datetime.utcnow().date().isoformat() + " - " + merge_request['title'],
  "labels": "cicd",
  "remove_source_branch": config.delete_source_branch
}

response = requests.request("POST", url, headers=headers, data=payload)

if response.status_code not in [200,201] :
  print(f'StatusCode: {response.status_code}')
  print(f'Response: {response.content}')
  raise  Exception(f'Gitlab server returned error')  

json_response = response.json()



concourse_response = {
  "version": config.version,
  "metadata": [
    { "name": "title", "value": merge_request['title'] },
    { "name": "source_branch", "value": config.source_branch }
  ]
}

print(concourse_response)