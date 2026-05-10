import argparse
import requests
import json
import time
from urllib.parse import urljoin

  class ArgoCDMonitor:
    def __init__(self, server_url, token, insecure=True):
        self.server_url = server_url.rstrip('/')
        self.headers = {'Authorization': f'Bearer {token}'}
        self.verify = not insecure
    def list_applications(self):
        url = urljoin(self.server_url, '/api/v1/applications')
        resp = requests.get(url, headers=self.headers, verify=self.verify)
        resp.raise_for_status()
        return resp.json().get('items', [])
