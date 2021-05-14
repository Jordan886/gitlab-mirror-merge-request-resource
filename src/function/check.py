#! /usr/bin/python3
import sys
import requests
import json
import datetime
import urllib.parse
from pprint import pprint
from load_json import LoadJson

# Load config 
config = LoadJson(sys.stdin)

# Only merge request of this day will be returned
# yesterday = datetime.date.today() - datetime.timedelta(days=1)
# print(yesterday.day)

project_id = urllib.parse.quote(config.project,safe='')

current_day = datetime.datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0).isoformat()

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

# print(json.dumps(check_response))

json_response = response.json()

wanted_keys=['id','title','project_id','source_branch']
check_response = []

for merge_request in json_response:
  simple_merge={}
  for key,value in merge_request.items():
    if key in wanted_keys:
      simple_merge[key] = value
  check_response.append(simple_merge)

print(check_response)

# print(json.dumps(check_response))