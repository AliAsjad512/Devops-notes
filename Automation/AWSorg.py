import boto3
import argparse
import datetime
import json
from collections import defaultdict

class AWSOrgReport:
    def __init__(self, region='us-east-1'):
        self.org = boto3.client('organizations')
        self.ce = boto3.client('ce', region_name=region)
        self.config = boto3.client('config', region_name=region)
    def list_accounts(self):
        accounts = []
        paginator = self.org.get_paginator('list_accounts')
        for page in paginator.paginate():
            accounts.extend(page['Accounts'])
        return accounts
    def get_account_cost(self, account_id, days=30):
        end = datetime.date.today()
        start = end - datetime.timedelta(days=days)
        try:
            response = self.ce.get_cost_and_usage(
                TimePeriod={'Start': start.strftime('%Y-%m-%d'), 'End': end.strftime('%Y-%m-%d')},
                Granularity='DAILY',
                Metrics=['UnblendedCost'],
                Filter={'Dimensions': {'Key': 'LINKED_ACCOUNT', 'Values': [account_id]}}
            )
            total = sum(float(day['Total']['UnblendedCost']['Amount']) for day in response['ResultsByTime'])
            return round(total, 2)
        except:
            return None
    def get_compliance_status(self, account_id):
        # Simplified: count of non-compliant rules
        try:
            response = self.config.get_compliance_details_by_config_rule(
                ComplianceTypes=['NON_COMPLIANT'],
                Limit=1
            )
            # Actually this is org-wide; for per-account you'd need AWS Config aggregator
            return "Unknown"
        except:
            return "Not enabled"
    def generate_report(self):
        accounts = self.list_accounts()
        report = []
        for acc in accounts:
            report.append({
                'Id': acc['Id'],
                'Name': acc['Name'],
                'Email': acc['Email'],
                'Status': acc['Status'],
                'CostLast30Days': self.get_account_cost(acc['Id']),
                'Compliance': self.get_compliance_status(acc['Id'])
            })
        return report