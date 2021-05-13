import json

class LoadJson:

  def __init__(self, payload):
    self.data = json.load(payload)
    self.source = self.data['source']
    try:
      self.api_url = self.source['api_url']
      self.access_token = self.source['access_token']
    except:
      raise Exception("Missing required source config")
    # check if also params exist
    if 'params' in self.data :
      self.params = self.data['params']
      try:
        self.project = self.params['project']
        self.source_branch = self.params['source_branch']
        self.target_branch = self.params['target_branch']
        self.title = self.params['title']
      except:
        raise Exception("Missing parameters")
