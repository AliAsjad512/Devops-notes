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

