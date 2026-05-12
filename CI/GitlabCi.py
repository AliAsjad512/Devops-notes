import argparse
import requests
import json
import sys

class GitLabPipelineTrigger:
    def __init__(self, project_id, token, gitlab_url='https://gitlab.com'):
        self.url = f"{gitlab_url.rstrip('/')}/api/v4/projects/{project_id}/trigger/pipeline"
        self.token = token