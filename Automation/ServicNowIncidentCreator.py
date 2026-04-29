import argparse
import requests
import json
from datetime import datetime

class ServiceNowIncident:
    def __init__(self, instance, username, password):
        self.url = f'https://{instance}.service-now.com/api/now/table/incident'
        self.auth = (username, password)
        self.headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
