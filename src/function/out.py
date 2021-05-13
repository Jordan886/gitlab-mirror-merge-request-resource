#! /usr/bin/python3
import os
import sys
import requests
import urllib.parse
from pprint import pprint
from datetime import datetime
from load_json import LoadJson

out_response = []
# Load config 
config = LoadJson(sys.stdin)

#If project name contains spaces or special character
project_id = urllib.parse.quote(config.project)

# Title will have datestamp at the beginning to avoid conflicts
title_suffix = datetime.now().isoformat(timespec='seconds')
title_complete = title_suffix + '' + config.title

# Prepare GitlabRequest
params = ''

url = 'https://' + config.api_url + '/api/v4/projects' + project_id + 'merge_requests' +  params
headers = {
  'Authorization': f'Bearer {config.access_token}'
}
payload={
  "id": project_id,
  "source_branch": config.source_branch,
  "target_branch": config.target_branch,
  "title": config.title
}

print(url,headers,payload)

# response = requests.request("POST", url, headers=headers, data=payload)


# if response.status_code != 200 :
#   print(f'StatusCode: {response.status_code}')
#   print(f'Response: {response.content}')
#   raise  Exception(f'Gitlab server returned error')
