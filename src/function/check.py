#! /usr/bin/python3
import sys
import requests
import json
from pprint import pprint
from load_json import LoadJson

check_response = []
# Load config 
config = LoadJson(sys.stdin)
# Prepare GitlabRequest
params = '?' + 'scope=all' + '&view=simple' + '&state=opened'
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

print(json.dumps(check_response))

