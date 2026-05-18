import argparse
import requests
import json

class NewRelicAlertManager:
    def __init__(self, api_key, account_id, region='us'):
        self.api_key = api_key
        self.account_id = account_id
        self.base_url = f'https://{region}.api.newrelic.com/graphql'
    def _graphql_request(self, query, variables=None):
        headers = {'API-Key': self.api_key, 'Content-Type': 'application/json'}
        payload = {'query': query, 'variables': variables}
        resp = requests.post(self.base_url, headers=headers, json=payload)
        resp.raise_for_status()
        return resp.json()
    def list_policies(self):
        query = """
        query ($accountId: Int!) {
          actor {
            account(id: $accountId) {
              alerts {
                policiesSearch {
                  policies {
                    id
                    name
                    incidentPreference
                  }
                }
              }
            }
          }
        }
        """
        result = self._graphql_request(query, {'accountId': int(self.account_id)})
        policies = result['data']['actor']['account']['alerts']['policiesSearch']['policies']
        return policies
