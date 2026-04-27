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
      def realtime_tail(self, function_name, interval=2):
        """Continuously stream new logs"""
        log_group_name = f'/aws/lambda/{function_name}'
        # Get the latest log stream
        stream_name = None
        last_timestamp = 0
        print(f"Tailing logs for {function_name} (Ctrl+C to stop)")
        try:
            while True:
                streams = self.logs.describe_log_streams(
                    logGroupName=log_group_name,
                    orderBy='LastEventTime',
                    descending=True,
                    limit=1
                )
                if streams['logStreams']:
                    new_stream = streams['logStreams'][0]['logStreamName']
                    if new_stream != stream_name:
                        stream_name = new_stream
                        last_timestamp = 0
                    # Get new events
                    resp = self.logs.get_log_events(
                        logGroupName=log_group_name,
                        logStreamName=stream_name,
                        startTime=last_timestamp + 1,
                        startFromHead=True
                    )
                    for event in resp['events']:
                        ts = datetime.datetime.fromtimestamp(event['timestamp']/1000).isoformat()
                        print(f"[{ts}] {event['message'].strip()}")
                        last_timestamp = event['timestamp']
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n🛑 Stopped tailing")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AWS Lambda Logs Tailer')
    parser.add_argument('function', help='Lambda function name')
    parser.add_argument('--region', default='us-east-1')
    parser.add_argument('--lines', type=int, default=100, help='Number of recent lines')
    parser.add_argument('--follow', action='store_true', help='Real-time tail')
    args = parser.parse_args()

    tailer = LambdaLogTailer(args.region)
    if args.follow:
        tailer.realtime_tail(args.function)
    else:
        tailer.tail_function(args.function, args.lines)
