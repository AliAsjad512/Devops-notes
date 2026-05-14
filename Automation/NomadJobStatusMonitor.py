import argparse
import requests
import json

 class NomadMonitor:
    def __init__(self, addr='http://localhost:4646'):
        self.addr = addr.rstrip('/')

    def list_jobs(self):
        resp = requests.get(f"{self.addr}/v1/jobs")
        resp.raise_for_status()
        return resp.json()
    
    def get_job_status(self, job_id):
        resp = requests.get(f"{self.addr}/v1/job/{job_id}")
        resp.raise_for_status()
        return resp.json()