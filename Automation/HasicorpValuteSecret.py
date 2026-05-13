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
