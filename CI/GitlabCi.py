import argparse
import requests
import json
import sys

class GitLabPipelineTrigger:
    def __init__(self, project_id, token, gitlab_url='https://gitlab.com'):
        self.url = f"{gitlab_url.rstrip('/')}/api/v4/projects/{project_id}/trigger/pipeline"
        self.token = token
    def trigger(self, ref='main', variables=None):
        payload = {'token': self.token, 'ref': ref}
        if variables:
            payload['variables'] = variables
        resp = requests.post(self.url, data=payload)
        if resp.status_code == 201:
            data = resp.json()
            print(f"✅ Pipeline triggered: {data['web_url']}")
            return data
        else:
            print(f"❌ Failed: {resp.text}")
            return None
    def get_pipeline_status(self, pipeline_id):
        url = f"{self.url.replace('/trigger/pipeline', '')}/pipelines/{pipeline_id}"
        resp = requests.get(url, headers={'PRIVATE-TOKEN': self.token})
        return resp.json().get('status')
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='GitLab CI Pipeline Trigger')
    parser.add_argument('--project', required=True, help='GitLab project ID')
    parser.add_argument('--token', required=True, help='Pipeline trigger token')
    parser.add_argument('--ref', default='main')
    parser.add_argument('--var', nargs='*', help='Variables as KEY=VALUE')
    parser.add_argument('--wait', action='store_true', help='Wait for completion')
    args = parser.parse_args()
    variables = {}
    if args.var:
        for v in args.var:
            key, val = v.split('=', 1)
            variables[key] = val

    trigger = GitLabPipelineTrigger(args.project, args.token)
    result = trigger.trigger(args.ref, variables)
    if result and args.wait:
        import time
    pipeline_id = result['id']
        while True:
            status = trigger.get_pipeline_status(pipeline_id)
            print(f"Status: {status}")
            if status in ('success', 'failed', 'canceled'):
                break
            time.sleep(5)
        sys.exit(0 if status == 'success' else 1)