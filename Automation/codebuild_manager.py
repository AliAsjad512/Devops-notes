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

        def start_build(self, project_name, source_version=None):
        """Trigger a build."""
        kwargs = {'projectName': project_name}
        if source_version:
            kwargs['sourceVersion'] = source_version
        response = self.codebuild.start_build(**kwargs)
        build_id = response['build']['id']
        print(f"Build started: {build_id}")
        return build_id
    
    def get_build_status(self, build_id):
        """Poll build status."""
        response = self.codebuild.batch_get_builds(ids=[build_id])
        build = response['builds'][0]
        return build['buildStatus'], build.get('logs', {}).get('deepLink')
    def wait_for_build(self, build_id, timeout=600):
        """Wait until build completes."""
        elapsed = 0
        while elapsed < timeout:
            status, log_url = self.get_build_status(build_id)
            print(f"Status: {status}")
            if status in ('SUCCEEDED', 'FAILED', 'FAULT', 'TIMED_OUT'):
                print(f"Logs: {log_url}")
                return status
            time.sleep(5)
            elapsed += 5
        return 'TIMED_OUT'
    

    if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--region', default='us-east-1')
    subparsers = parser.add_subparsers(dest='cmd', required=True)

    create = subparsers.add_parser('create')
    create.add_argument('--name', required=True)
    create.add_argument('--repo', required=True)
    create.add_argument('--buildspec', default='buildspec.yml')
    create.add_argument('--role', required=True)

    start = subparsers.add_parser('start')
    start.add_argument('--project', required=True)
    start.add_argument('--version', help='Git branch/commit')

    wait = subparsers.add_parser('wait')
    wait.add_argument('--build-id', required=True)

    args = parser.parse_args()
    mgr = CodeBuildManager(args.region)

    if args.cmd == 'create':
        mgr.create_project(args.name, args.repo, args.buildspec, args.role)
    elif args.cmd == 'start':
        build_id = mgr.start_build(args.project, args.version)
    elif args.cmd == 'wait':
        status = mgr.wait_for_build(args.build_id)
        sys.exit(0 if status == 'SUCCEEDED' else 1)
