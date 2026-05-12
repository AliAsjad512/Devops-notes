import argparse
import requests
import json
import sys

class GitLabPipelineTrigger:
    def __init__(self, project_id, token, gitlab_url='https://gitlab.com'):
        self.url = f"{gitlab_url.rstrip('/')}/api/v4/projects/{project_id}/trigger/pipeline"
        self.token = token
    def trigger(self, ref='main', variables=None):
        payload = {'token': self.token, 'ref': ref}
        if variables:
            payload['variables'] = variables
        resp = requests.post(self.url, data=payload)
        if resp.status_code == 201:
            data = resp.json()
            print(f"✅ Pipeline triggered: {data['web_url']}")
            return data
        else:
            print(f"❌ Failed: {resp.text}")
            return None