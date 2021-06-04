#! /usr/local/bin/python3
from posixpath import join
import sys
import os
import requests
import json
from datetime import datetime
import urllib.parse
from load_json import LoadJson

# Load config 
config = LoadJson(sys.stdin)

# Gitlab API wants projectID urlencoded when using names
project_id = urllib.parse.quote(config.project,safe='')

# The filepath will be passed as argument
source_path = sys.argv[1]

# Function for finding in source path which directory holds merge_list.json
# Next() will walk only in the first directory level
def find_merge_file(base_path):
  try:
    folders=next(os.walk(base_path))[1]
    for folder in folders:
      files = os.listdir(os.path.join(base_path,folder))
      for file in files:
        if 'merge_list.json' in file:
          merge_file_path = os.path.join(base_path,folder,file)
          return merge_file_path
  except:    
    raise Exception(f'No input file found in {base_path}, this could be a bug or misconfig)')

source = find_merge_file(source_path)

try:
  with open(source) as merge_file:
    merge_request = json.loads(merge_file.read())
except:
  raise Exception(f'file {source} not found')

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
  "version": {"iid": str(json_response['iid'])},
  "metadata": [
    { "name": "title", "value": merge_request['title'] },
    { "name": "source_branch", "value": config.source_branch }
  ]
}

print(json.dumps(concourse_response))