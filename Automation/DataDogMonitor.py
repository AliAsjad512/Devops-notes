import argparse
import requests
import json
import sys

class DatadogMonitorManager:
    def __init__(self, api_key, app_key, site='datadoghq.com'):
        self.api_key = api_key
        self.app_key = app_key
        self.base_url = f'https://api.{site}/api/v1'
    def _headers(self):
        return {
            'DD-API-KEY': self.api_key,
            'DD-APPLICATION-KEY': self.app_key,
            'Content-Type': 'application/json'
        }