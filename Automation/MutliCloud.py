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
class GCPSecretManager:
    def __init__(self, project_id):
        self.client = secretmanager.SecretManagerServiceClient()
        self.project_id = project_id

    def get_secret(self, secret_name):
        name = f"projects/{self.project_id}/secrets/{secret_name}/versions/latest"
        try:
            response = self.client.access_secret_version(name=name)
            return response.payload.data.decode('UTF-8')
        except:
            return None

    def put_secret(self, secret_name, value):
        parent = f"projects/{self.project_id}"
        try:
            self.client.create_secret(parent=parent, secret_id=secret_name, secret={'replication': {'automatic': {}}})
        except:
            pass
        name = f"{parent}/secrets/{secret_name}"
        self.client.add_secret_version(parent=name, payload={'data': value.encode('UTF-8')})

    def list_secrets(self, prefix=''):
        parent = f"projects/{self.project_id}"
        secrets = self.client.list_secrets(parent=parent)
        return [s.name.split('/')[-1] for s in secrets if s.name.split('/')[-1].startswith(prefix)]

class AzureKeyVault:
    def __init__(self, vault_url):
        self.client = SecretClient(vault_url=vault_url, credential=DefaultAzureCredential())

    def get_secret(self, secret_name):
        try:
            return self.client.get_secret(secret_name).value
        except:
            return None

    def put_secret(self, secret_name, value):
        self.client.set_secret(secret_name, value)

    def list_secrets(self, prefix=''):
        secrets = self.client.list_properties_of_secrets()
        return [s.name for s in secrets if s.name.startswith(prefix)]