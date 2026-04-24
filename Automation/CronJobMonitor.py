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
