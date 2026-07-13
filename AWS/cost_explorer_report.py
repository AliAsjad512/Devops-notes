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