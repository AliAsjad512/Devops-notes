import argparse
import hvac
import json
import sys

class VaultSecretManager:
    def __init__(self, url, token=None, role_id=None, secret_id=None):
        self.client = hvac.Client(url=url, token=token)
        if not self.client.is_authenticated():
            if role_id and secret_id:
                self.client.auth.approle.login(role_id=role_id, secret_id=secret_id)
            else:
                raise Exception("Authentication failed")
    def write_secret(self, path, data, mount='secret'):
        self.client.secrets.kv.v2.create_or_update_secret(mount_point=mount, path=path, secret=data)
        print(f"✅ Secret written to {mount}/{path}")
    def read_secret(self, path, mount='secret'):
        try:
            resp = self.client.secrets.kv.v2.read_secret_version(mount_point=mount, path=path)
            return resp['data']['data']
        except hvac.exceptions.InvalidPath:
            print(f"❌ Secret not found at {mount}/{path}")
            return None
    def delete_secret(self, path, mount='secret'):
        self.client.secrets.kv.v2.delete_latest_version_of_secret(mount_point=mount, path=path)
        print(f"🗑️ Secret deleted from {mount}/{path}")
    def list_secrets(self, path='', mount='secret'):
        try:
            resp = self.client.secrets.kv.v2.list_secrets(mount_point=mount, path=path)
            return resp['data']['keys']
        except:
            return []
        
    if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Vault Secret Manager')
    parser.add_argument('--url', required=True, help='Vault URL')
    parser.add_argument('--token', help='Vault token')
    parser.add_argument('--role-id', help='AppRole role_id')
    parser.add_argument('--secret-id', help='AppRole secret_id')
    parser.add_argument('--action', choices=['write', 'read', 'delete', 'list'], required=True)
    parser.add_argument('--path', required=True, help='Secret path (e.g., myapp/db)')
    parser.add_argument('--data', help='JSON data for write')
    parser.add_argument('--mount', default='secret')
    args = parser.parse_args()

    mgr = VaultSecretManager(args.url, args.token, args.role_id, args.secret_id)
    if args.action == 'write':
        if not args.data:
            print("❌ --data required for write")
            sys.exit(1)
        data = json.loads(args.data)
        mgr.write_secret(args.path, data, args.mount)
    elif args.action == 'read':
        secret = mgr.read_secret(args.path, args.mount)
        if secret:
            print(json.dumps(secret, indent=2))
    elif args.action == 'delete':
        mgr.delete_secret(args.path, args.mount)
    elif args.action == 'list':
        keys = mgr.list_secrets(args.path, args.mount)
        for key in keys:
            print(key)

