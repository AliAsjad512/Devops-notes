import subprocess
import argparse
import logging
import sys
import os
from pathlib import Path

class SSLRenewer:
    def __init__(self, certbot_path='certbot'):
        self.certbot = certbot_path
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def check_cert_expiry(self, domain):
        """Check certificate expiry using openssl"""
        try:
            result = subprocess.run(
                ['openssl', 's_client', '-servername', domain, '-connect', f'{domain}:443'],
                input='QUIT\n', text=True, capture_output=True, timeout=10
            )
            # Extract expiry from output (simplified)
            for line in result.stderr.split('\n'):
                if 'notAfter=' in line:
                    return line.split('notAfter=')[1]
            return None
        except Exception as e:
            self.logger.error(f"Failed to check cert for {domain}: {e}")
            return None

