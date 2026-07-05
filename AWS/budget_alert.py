import boto3
import argparse
import json

class BudgetManager:
    def __init__(self, account_id, region='us-east-1'):
        self.budget = boto3.client('budgets')
        self.account_id = account_id
     def create_budget(self, budget_name, limit_amount, limit_unit='USD', time_unit='MONTHLY', email=None):
          payload = {
            'AccountId': self.account_id,
            'Budget': {
                'BudgetName': budget_name,
                'BudgetLimit': {'Amount': str(limit_amount), 'Unit': limit_unit},
                'TimeUnit': time_unit,
                'BudgetType': 'COST',
                'CostFilters': {'Service': ['AmazonS3']}  # optional filter
            },

            'NotificationsWithSubscribers': [{
                'Notification': {
                    'NotificationType': 'ACTUAL',
                    'ComparisonOperator': 'GREATER_THAN',
                    'Threshold': 80,
                    'ThresholdType': 'PERCENTAGE'
                },

                 'Subscribers': [{'SubscriptionType': 'EMAIL', 'Address': email}]
            }]
        }
           response = self.budget.create_budget(**payload)
        print(f"Budget {budget_name} created with {limit_amount} {limit_unit} limit")