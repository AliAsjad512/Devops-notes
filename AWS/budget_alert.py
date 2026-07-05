import boto3
import argparse
import json

class BudgetManager:
    def __init__(self, account_id, region='us-east-1'):
        self.budget = boto3.client('budgets')
        self.account_id = account_id