import argparse
import requests
import json

class NewRelicAlertManager:
    def __init__(self, api_key, account_id, region='us'):
        self.api_key = api_key
        self.account_id = account_id
        self.base_url = f'https://{region}.api.newrelic.com/graphql'