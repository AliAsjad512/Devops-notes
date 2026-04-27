import boto3
import argparse
import time
import datetime
import threading
from collections import deque
 
 class LambdaLogTailer:
    def __init__(self, region='us-east-1'):
        self.logs = boto3.client('logs', region_name=region)
        self.tailers = {}