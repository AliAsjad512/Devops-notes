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
    def get_app_status(self, app_name):
        url = urljoin(self.server_url, f'/api/v1/applications/{app_name}')
        resp = requests.get(url, headers=self.headers, verify=self.verify)
        resp.raise_for_status()
        return resp.json()
      def get_out_of_sync_apps(self):
        apps = self.list_applications()
        out_of_sync = []
        for app in apps:
            status = app.get('status', {})
            sync_status = status.get('sync', {}).get('status', '')
            health_status = status.get('health', {}).get('status', '')
            if sync_status != 'Synced' or health_status != 'Healthy':
                out_of_sync.append({
                    'name': app['metadata']['name'],
                    'sync_status': sync_status,
                    'health_status': health_status,
                    'destination': app['spec']['destination']
                })
        return out_of_sync
    def sync_app(self, app_name, revision='HEAD', dry_run=False):
        url = urljoin(self.server_url, f'/api/v1/applications/{app_name}/sync')
        payload = {'revision': revision, 'dryRun': dry_run, 'prune': True, 'strategy': {'force': False}}
        resp = requests.post(url, headers=self.headers, json=payload, verify=self.verify)
        resp.raise_for_status()
        return resp.json()
    
    if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ArgoCD Sync Checker')
    parser.add_argument('--server', required=True, help='ArgoCD server URL')
    parser.add_argument('--token', required=True, help='API token')
    parser.add_argument('--action', choices=['list', 'check', 'sync'], default='check')
    parser.add_argument('--app', help='Application name for sync')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    monitor = ArgoCDMonitor(args.server, args.token)
    if args.action == 'list':
        apps = monitor.list_applications()
        for app in apps:
            print(app['metadata']['name'])
    elif args.action == 'check':
        out_of_sync = monitor.get_out_of_sync_apps()
        if out_of_sync:
            print(f"❌ Found {len(out_of_sync)} applications out of sync or unhealthy:")
            for app in out_of_sync:
                print(f"  - {app['name']}: sync={app['sync_status']}, health={app['health_status']}")
        else:
            print("✅ All applications are synced and healthy")
    elif args.action == 'sync':
        if not args.app:
            print("❌ --app required for sync action")
            exit(1)
        result = monitor.sync_app(args.app, dry_run=args.dry_run)
        print(f"Sync initiated for {args.app}: {result.get('status', 'unknown')}")

