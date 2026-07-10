import boto3
import argparse
import time
import sys

class CodeBuildManager:
    def __init__(self, region='us-east-1'):
        self.codebuild = boto3.client('codebuild', region_name=region)

        def create_project(self, name, source_repo, buildspec, service_role):
        """Create a CodeBuild project from a source repo."""
        response = self.codebuild.create_project(
            name=name,
            source={'type': 'GITHUB', 'location': source_repo, 'buildspec': buildspec},
            artifacts={'type': 'NO_ARTIFACTS'},
            environment={'type': 'LINUX_CONTAINER', 'image': 'aws/codebuild/amazonlinux2-x86_64-standard:4.0', 'computeType': 'BUILD_GENERAL1_SMALL'},
            serviceRole=service_role
        )
        print(f"Project {name} created: {response['project']['arn']}")