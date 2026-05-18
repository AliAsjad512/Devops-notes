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
    
    def create_policy(self, name, incident_preference='PER_POLICY'):
        mutation = """
        mutation ($accountId: Int!, $name: String!, $incidentPreference: AlertPolicyIncidentPreference!) {
          alertsPolicyCreate(accountId: $accountId, name: $name, incidentPreference: $incidentPreference) {
            id
            name
          }
        }
        """
        vars = {'accountId': int(self.account_id), 'name': name, 'incidentPreference': incident_preference}
        result = self._graphql_request(mutation, vars)
        return result['data']['alertsPolicyCreate']
    def delete_policy(self, policy_id):
        mutation = """
        mutation ($accountId: Int!, $id: Int!) {
          alertsPolicyDelete(accountId: $accountId, id: $id) {
            id
          }
        }
        """
        result = self._graphql_request(mutation, {'accountId': int(self.account_id), 'id': int(policy_id)})
        return result['data']['alertsPolicyDelete']
    
    if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='New Relic Alert Manager')
    parser.add_argument('--api-key', required=True)
    parser.add_argument('--account-id', required=True)
    parser.add_argument('--action', choices=['list', 'create', 'delete'], required=True)
    parser.add_argument('--name', help='Policy name')
    parser.add_argument('--policy-id', help='Policy ID for delete')
    args = parser.parse_args()

    manager = NewRelicAlertManager(args.api_key, args.account_id)
    if args.action == 'list':
        policies = manager.list_policies()
        for p in policies:
            print(f"{p['id']}: {p['name']}")
    elif args.action == 'create':
        policy = manager.create_policy(args.name)
        print(f"✅ Created policy: {policy['id']} - {policy['name']}")
    elif args.action == 'delete':
        manager.delete_policy(args.policy_id)
        print(f"🗑️ Deleted policy {args.policy_id}")



