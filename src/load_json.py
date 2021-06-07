import json

class LoadJson:

  def __init__(self, payload):
    self.data = json.load(payload)
    self.source = self.data['source']
    try:
      self.api_url = self.source['api_url']
      self.access_token = self.source['access_token']
      self.project = self.source['project']
      self.branch = self.source['branch']
    except:
      raise Exception("Missing required source config")
    # check if also params exist
    if 'params' in self.data :
      self.params = self.data['params']
      try:
        self.target_branch = self.params['target_branch']
        # Optional params
        if 'delete_source' in self.params:
          self.delete_source_branch = self.params['delete_source']
      except:
        raise Exception("Missing parameters")
    # version is passed in get and put steps
    if 'version' in self.data :
      self.version = self.data['version']
      try:
        self.id = self.version['iid']
      except:
        raise Exception("Version not set")        
