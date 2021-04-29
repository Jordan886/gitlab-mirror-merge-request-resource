import json

class LoadJson:

  def __init__(self, payload):
    self.data = json.load(payload)['source']
  # PARAMS VALIDATION
    try:
      self.api_url = self.data['api_url']
      self.access_token = self.data['access_token']
      self.source_branch = self.data['password']
      self.target_branch = self.data['channel']
    except:
      raise Exception("Wrong parameters")
