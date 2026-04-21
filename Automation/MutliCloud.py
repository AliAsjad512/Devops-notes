import argparse
import json
import boto3
from google.cloud import secretmanager
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import base64
class SecretSynchronizer:
    def __init__(self, source_cloud, source_config, dest_cloud, dest_config):
        self.source = self._connect(source_cloud, source_config)
        self.dest = self._connect(dest_cloud, dest_config)
        self.source_cloud = source_cloud
        self.dest_cloud = dest_cloud
    def _connect(self, cloud, config):
        if cloud == 'aws':
            return AWSSecretManager(config['region'])
        elif cloud == 'gcp':
            return GCPSecretManager(config['project_id'])
        elif cloud == 'azure':
            return AzureKeyVault(config['vault_url'])
        else:
            raise ValueError(f"Unsupported cloud: {cloud}")
    def sync_secret(self, secret_name):
        """Sync a single secret from source to destination"""
        secret_value = self.source.get_secret(secret_name)
        if secret_value:
            self.dest.put_secret(secret_name, secret_value)
            print(f"✅ Synced {secret_name} from {self.source_cloud} to {self.dest_cloud}")
        else:
            print(f"❌ Secret {secret_name} not found in {self.source_cloud}")
    def sync_all(self, prefix=''):
        """Sync all secrets matching prefix"""
        secrets = self.source.list_secrets(prefix)
        for secret in secrets:
            self.sync_secret(secret)

class AWSSecretManager:
    def __init__(self, region):
        self.client = boto3.client('secretsmanager', region_name=region)

    def get_secret(self, secret_name):
        try:
            response = self.client.get_secret_value(SecretId=secret_name)
            return response['SecretString']
        except:
            return None

    def put_secret(self, secret_name, value):
        self.client.create_secret(Name=secret_name, SecretString=value, ForceOverwriteReplicaSecret=True)

    def list_secrets(self, prefix=''):
        response = self.client.list_secrets()
        return [s['Name'] for s in response['SecretList'] if s['Name'].startswith(prefix)]
