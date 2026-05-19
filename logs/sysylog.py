import socketserver
import argparse
import json
import logging
from datetime import datetime

class SyslogHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        timestamp = datetime.utcnow().isoformat()
        try:
            message = data.decode('utf-8')
        except:
            message = str(data)
        log_entry = {
            'timestamp': timestamp,
            'host': self.client_address[0],
            'message': message
        }
        # Write to file or forward
        with open('syslog.json', 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        print(f"Received: {log_entry['host']} - {log_entry['message'][:100]}")
class SyslogServer:
    def __init__(self, host='0.0.0.0', port=514):
        self.host = host
        self.port = port
