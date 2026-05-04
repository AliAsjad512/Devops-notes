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
    def save_logs(self, logs, output_file, compress=False):
        data = {'timestamp': datetime.utcnow().isoformat(), 'logs': logs}
        if compress:
            with gzip.open(output_file + '.gz', 'wt', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            print(f"✅ Saved compressed logs to {output_file}.gz")
        else:
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"✅ Saved logs to {output_file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Docker Log Collector')
    parser.add_argument('--label', help='Filter containers by label')
    parser.add_argument('--name', help='Filter by name pattern')
    parser.add_argument('--since', help='Since timestamp (e.g., "2025-01-01T00:00:00")')
    parser.add_argument('--tail', type=int, default=1000)
    parser.add_argument('--output', default='docker_logs.json')
    parser.add_argument('--compress', action='store_true')
    args = parser.parse_args()

    collector = DockerLogCollector()
    since = None
    if args.since:
        since = datetime.fromisoformat(args.since)
    logs = collector.collect_all(label_filter=args.label, name_filter=args.name, since=since, tail=args.tail)
    collector.save_logs(logs, args.output, args.compress)

