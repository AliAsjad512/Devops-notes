import subprocess
import json
import argparse
import datetime
import smtplib
from email.mime.text import MIMEText
from pathlib import Path

class CronMonitor:
    def __init__(self, log_file='/var/log/cron.log'):
        self.log_file = Path(log_file)
    def parse_cron_log(self, hours=24):
        """Parse cron log for the last N hours"""
        if not self.log_file.exists():
            return []
        cutoff = datetime.datetime.now() - datetime.timedelta(hours=hours)
        jobs = {}
        with open(self.log_file, 'r') as f:
            for line in f:
                # Example: Mar 20 10:30:01 hostname CRON[12345]: (user) CMD (command)
                try:
                    parts = line.strip().split()
                    if len(parts) < 5:
                        continue
                    timestamp_str = ' '.join(parts[:3])
                    timestamp = datetime.datetime.strptime(timestamp_str + ' ' + str(datetime.datetime.now().year), '%b %d %H:%M:%S %Y')
                    if timestamp < cutoff:
                        continue
                    if 'CMD' in line:
                        cmd = line.split('CMD (')[1].rstrip(')')
                        job_key = cmd
                        if job_key not in jobs:
                            jobs[job_key] = {'runs': [], 'failures': []}
                        jobs[job_key]['runs'].append(timestamp)
                    elif 'FAILED' in line or 'error' in line.lower():
                        # Heuristic for failure detection
                        cmd = line.split('CMD (')[1].rstrip(')') if 'CMD' in line else 'unknown'
                        if cmd in jobs:
                            jobs[cmd]['failures'].append(timestamp)
                except:
                    continue
        return jobs
