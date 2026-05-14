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
    def get_allocations(self, job_id):
        resp = requests.get(f"{self.addr}/v1/job/{job_id}/allocations")
        resp.raise_for_status()
        return resp.json()
    def check_failed_allocations(self):
        jobs = self.list_jobs()
        failed = []
        for job in jobs:
            job_id = job['ID']
            allocs = self.get_allocations(job_id)
            for alloc in allocs:
                if alloc['ClientStatus'] not in ('running', 'complete'):
                    failed.append({
                        'job_id': job_id,
                        'alloc_id': alloc['ID'],
                        'status': alloc['ClientStatus']
                    })
        return failed
