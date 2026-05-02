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

