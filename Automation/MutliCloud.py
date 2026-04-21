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