import docker
import argparse
import time
import gzip
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

class DockerLogCollector:
    def __init__(self):
        self.client = docker.from_env()
    def get_containers(self, label_filter=None, name_filter=None):
        filters = {}
        if label_filter:
            filters['label'] = label_filter
        if name_filter:
            filters['name'] = name_filter
        return self.client.containers.list(filters=filters)
