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
    def check_missed_jobs(self, expected_interval_minutes=60):
        """Check if jobs ran within expected interval"""
        jobs = self.parse_cron_log(24)
        missed = []
        for job, data in jobs.items():
            if not data['runs']:
                missed.append({'job': job, 'reason': 'No runs in last 24h'})
            else:
                last_run = max(data['runs'])
                minutes_since = (datetime.datetime.now() - last_run).total_seconds() / 60
                if minutes_since > expected_interval_minutes * 1.5:
                    missed.append({'job': job, 'last_run': last_run.isoformat(), 'minutes_since': round(minutes_since)})
        return missed
    def send_alert(self, missed_jobs, email_config):
        """Send email alert for missed jobs"""
        if not missed_jobs:
            return
        body = "The following cron jobs may be missed:\n\n"
        for job in missed_jobs:
            body += f"- {job['job']}: {job.get('reason', f"Last run {job['minutes_since']} minutes ago")}\n"
        msg = MIMEText(body)
        msg['Subject'] = 'Cron Job Monitor Alert'
        msg['From'] = email_config['from']
        msg['To'] = email_config['to']
        with smtplib.SMTP(email_config['smtp_host'], email_config['smtp_port']) as server:
            if email_config.get('tls'):
                server.starttls()
            if email_config.get('user'):
                server.login(email_config['user'], email_config['password'])
            server.send_message(msg)
        print("✅ Alert sent")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Cron Job Monitor')
    parser.add_argument('--log', default='/var/log/syslog', help='Log file path')
    parser.add_argument('--interval', type=int, default=60, help='Expected interval (minutes)')
    parser.add_argument('--email-to', help='Email for alerts')
    parser.add_argument('--smtp-host', default='localhost')
    parser.add_argument('--smtp-port', type=int, default=25)
    args = parser.parse_args()

    monitor = CronMonitor(args.log)
    missed = monitor.check_missed_jobs(args.interval)
    if missed:
        print(f"⚠️ Found {len(missed)} potentially missed jobs")
        for job in missed:
            print(f"  - {job['job']}")
        if args.email_to:
            email_config = {
                'from': 'cron-monitor@localhost',
                'to': args.email_to,
                'smtp_host': args.smtp_host,
                'smtp_port': args.smtp_port
            }
            monitor.send_alert(missed, email_config)
    else:
        print("✅ All cron jobs appear to be running on schedule")
