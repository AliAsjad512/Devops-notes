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
    def list_monitors(self):
        resp = requests.get(f'{self.base_url}/monitor', headers=self._headers())
        resp.raise_for_status()
        return resp.json()
    def create_monitor(self, name, query, type='metric alert', message='Alert triggered', options=None):
        payload = {
            'name': name,
            'type': type,
            'query': query,
            'message': message,
            'options': options or {'thresholds': {'critical': 80}}
        }
        resp = requests.post(f'{self.base_url}/monitor', headers=self._headers(), json=payload)
        resp.raise_for_status()
        print(f"✅ Monitor created: {resp.json()['id']}")
        return resp.json()
     def mute_monitor(self, monitor_id, scope=None):
        url = f'{self.base_url}/monitor/{monitor_id}/mute'
        payload = scope and {'scope': scope} or {}
        resp = requests.post(url, headers=self._headers(), json=payload)
        resp.raise_for_status()
        print(f"✅ Monitor {monitor_id} muted")
    def delete_monitor(self, monitor_id):
        resp = requests.delete(f'{self.base_url}/monitor/{monitor_id}', headers=self._headers())
        resp.raise_for_status()
        print(f"🗑️ Monitor {monitor_id} deleted")
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Datadog Monitor Manager')
    parser.add_argument('--api-key', required=True)
    parser.add_argument('--app-key', required=True)
    parser.add_argument('--action', choices=['list', 'create', 'mute', 'delete'], required=True)
    parser.add_argument('--name', help='Monitor name (for create)')
    parser.add_argument('--query', help='Monitor query (for create)')
    parser.add_argument('--monitor-id', type=int, help='Monitor ID')
    args = parser.parse_args()

    manager = DatadogMonitorManager(args.api_key, args.app_key)
    if args.action == 'list':
        monitors = manager.list_monitors()
        for m in monitors:
            print(f"{m['id']}: {m['name']} - {m['status']}")
    elif args.action == 'create':
        manager.create_monitor(args.name, args.query)
    elif args.action == 'mute':
        manager.mute_monitor(args.monitor_id)
    elif args.action == 'delete':
        manager.delete_monitor(args.monitor_id)
