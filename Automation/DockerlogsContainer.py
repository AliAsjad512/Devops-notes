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
    def collect_logs(self, container, since=None, tail=1000):
        kwargs = {'timestamps': True, 'tail': tail}
        if since:
            kwargs['since'] = int(since.timestamp())
        logs = container.logs(**kwargs).decode('utf-8', errors='ignore')
        return {
            'container_id': container.short_id,
            'container_name': container.name,
            'logs': logs,
            'collected_at': datetime.utcnow().isoformat()
        }
    def collect_all(self, label_filter=None, name_filter=None, since=None, tail=1000):
        containers = self.get_containers(label_filter, name_filter)
        logs = []
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(self.collect_logs, c, since, tail) for c in containers]
            for f in futures:
                logs.append(f.result())
        return logs
