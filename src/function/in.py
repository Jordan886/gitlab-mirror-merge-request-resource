#! /usr/bin/python3
import os
import sys
import requests
import json
from pprint import pprint
from load_json import LoadJson

in_response = []
# Load config 
config = LoadJson(sys.stdin)
destination_path = sys.argv[1]
# Prepare GitlabRequest
params = '?' + 'scope=all' + '&view=simple' + '&state=opened'
param2 = f'&source_branch={config.source_branch}' + f'&target_branch={config.target_branch}'
url = 'https://' + config.api_url + '/api/v4/merge_requests' + params
headers = {
  'Authorization': f'Bearer {config.access_token}'
}
payload={}

response = requests.request("GET", url, headers=headers, data=payload)


if response.status_code != 200 :
  print(f'StatusCode: {response.status_code}')
  print(f'Response: {response.content}')
  raise  Exception(f'Gitlab server returned error')  


destination = os.path.join(destination_path, 'merge_list.json')

with open(destination,'w') as file:
    json.dump(response.json(), file, indent=4)