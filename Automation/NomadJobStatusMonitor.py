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
    if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Nomad Job Monitor')
    parser.add_argument('--addr', default='http://localhost:4646')
    parser.add_argument('--action', choices=['list', 'status', 'failed'], default='list')
    parser.add_argument('--job', help='Job ID for status')
    args = parser.parse_args()

    monitor = NomadMonitor(args.addr)
    if args.action == 'list':
        jobs = monitor.list_jobs()
        for job in jobs:
            print(f"{job['ID']} - {job['Status']}")
    elif args.action == 'status':
        if not args.job:
            print("❌ --job required")
            exit(1)
        status = monitor.get_job_status(args.job)
        print(f"Job: {status['ID']}")
        print(f"Status: {status['Status']}")
        print(f"Submit Time: {status['SubmitTime']}")
    elif args.action == 'failed':
        failed = monitor.check_failed_allocations()
        if failed:
            print(f"❌ Found {len(failed)} failed allocations:")
            for f in failed:
                print(f"  - {f['job_id']}: {f['alloc_id']} ({f['status']})")
        else:
            print("✅ All allocations healthy")

