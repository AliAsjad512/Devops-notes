import argparse
import requests
import json
from datetime import datetime

class ServiceNowIncident:
    def __init__(self, instance, username, password):
        self.url = f'https://{instance}.service-now.com/api/now/table/incident'
        self.auth = (username, password)
        self.headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    def create_incident(self, short_description, description, category='infrastructure', impact=3, urgency=3, caller_id='admin'):
        """Create a new incident"""
        payload = {
            'short_description': short_description,
            'description': description,
            'category': category,
            'impact': impact,
            'urgency': urgency,
            'caller_id': caller_id,
            'state': 1,  # New
            'contact_type': 'monitoring'
        }
        resp = requests.post(self.url, auth=self.auth, headers=self.headers, json=payload)
        if resp.status_code == 201:
            incident = resp.json()['result']
            print(f"✅ Created ServiceNow incident: {incident['number']}")
            return incident
        else:
            print(f"❌ Failed to create incident: {resp.text}")
            return None
    def create_from_alert(self, alert_name, alert_details, severity='high', source='Prometheus'):
        """Create incident from monitoring alert"""
        severity_map = {'critical': 1, 'high': 2, 'medium': 3, 'low': 4}
        impact = severity_map.get(severity.lower(), 3)
        short = f"[{source}] {alert_name}"
        desc = f"Alert triggered at {datetime.utcnow().isoformat()}\n\nDetails:\n{alert_details}"
        return self.create_incident(short, desc, impact=impact, urgency=impact)
