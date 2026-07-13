import boto3
import argparse
import json
import csv
from datetime import datetime, timedelta
import sys
class CostExplorerReport:
    def __init__(self, region='us-east-1'):
        self.ce = boto3.client('ce', region_name=region)

def get_cost_by_service(self, days_back=30):
        end = datetime.now().date()
        start = end - timedelta(days=days_back)
        response = self.ce.get_cost_and_usage(
            TimePeriod={'Start': start.isoformat(), 'End': end.isoformat()},
            Granularity='MONTHLY',
            Metrics=['UnblendedCost'],
            GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
        )
        results = []
        for group in response['ResultsByTime'][0]['Groups']:
            service = group['Keys'][0]
            cost = float(group['Metrics']['UnblendedCost']['Amount'])
            results.append({'Service': service, 'CostUSD': round(cost, 2)})
        results.sort(key=lambda x: x['CostUSD'], reverse=True)
        return results

def get_cost_by_tag(self, tag_key, days_back=30):
        end = datetime.now().date()
        start = end - timedelta(days=days_back)
        response = self.ce.get_cost_and_usage(
            TimePeriod={'Start': start.isoformat(), 'End': end.isoformat()},
            Granularity='MONTHLY',
            Metrics=['UnblendedCost'],
            GroupBy=[{'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'}],
            Filter={'Tags': {'Key': tag_key, 'Values': ['*']}}
        )
        # ... parse similar
        return results

def save_csv(self, data, filename):
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        print(f"Saved to {filename}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', choices=['service', 'tag'], default='service')
    parser.add_argument('--tag-key', help='Tag key for type=tag')
    parser.add_argument('--days', type=int, default=30)
    parser.add_argument('--output', default='cost_report.csv')
    args = parser.parse_args()