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