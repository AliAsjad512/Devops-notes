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
