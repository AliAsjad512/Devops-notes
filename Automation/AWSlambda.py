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
    def tail_function(self, function_name, lines=100):
        """Tail logs for a Lambda function"""
        log_group_name = f'/aws/lambda/{function_name}'
        # Get log streams
        streams = self.logs.describe_log_streams(
            logGroupName=log_group_name,
            orderBy='LastEventTime',
            descending=True,
            limit=5
        )
        if not streams['logStreams']:
            print(f"No log streams found for {function_name}")
            return

        # Collect recent logs
        events = []
        for stream in streams['logStreams']:
            try:
                resp = self.logs.get_log_events(
                    logGroupName=log_group_name,
                    logStreamName=stream['logStreamName'],
                    limit=lines
                )
                events.extend(resp['events'])
            except:
                pass
        events.sort(key=lambda x: x['timestamp'])
        for event in events[-lines:]:
            ts = datetime.datetime.fromtimestamp(event['timestamp']/1000).isoformat()
            print(f"[{ts}] {event['message'].strip()}")
