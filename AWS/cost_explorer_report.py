import boto3
import argparse
import json
import csv
from datetime import datetime, timedelta
import sys
class CostExplorerReport:
    def __init__(self, region='us-east-1'):
        self.ce = boto3.client('ce', region_name=region)