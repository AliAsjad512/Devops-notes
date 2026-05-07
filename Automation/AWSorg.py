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