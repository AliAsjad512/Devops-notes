import argparse
import requests
import base64
import json

class AzureDevOpsPipeline:
    def __init__(self, org, project, pat):
        self.org = org
        self.project = project
        self.auth = base64.b64encode(f":{pat}".encode()).decode()
        self.headers = {
            'Authorization': f'Basic {self.auth}',
            'Content-Type': 'application/json'
        }
        self.base_url = f'https://dev.azure.com/{org}/{project}'
    def list_pipelines(self):
        """List all pipelines in the project"""
        url = f"{self.base_url}/_apis/pipelines?api-version=6.0-preview.1"
        resp = requests.get(url, headers=self.headers)
        return resp.json().get('value', [])
    def run_pipeline(self, pipeline_id, branch='main', parameters=None):
        """Trigger a pipeline run"""
        url = f"{self.base_url}/_apis/pipelines/{pipeline_id}/runs?api-version=6.0-preview.1"
        payload = {
            'resources': {'repositories': {'self': {'refName': f'refs/heads/{branch}'}}}
        }
        if parameters:
            payload['templateParameters'] = parameters
        resp = requests.post(url, headers=self.headers, json=payload)
        if resp.status_code == 200:
            run = resp.json()
            print(f"✅ Pipeline run started: {run['_links']['web']['href']}")
            return run
        else:
            print(f"❌ Failed to start pipeline: {resp.text}")
            return None
    def get_pipeline_run_status(self, run_id):
        """Get status of a pipeline run"""
        url = f"{self.base_url}/_apis/pipelines/runs/{run_id}?api-version=6.0-preview.1"
        resp = requests.get(url, headers=self.headers)
        return resp.json().get('state')
