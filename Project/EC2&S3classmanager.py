import boto3
import argparse
import sys

class AWSManager:
    def __init__(self, region='us-east-1'):
        self.ec2 = boto3.client('ec2', region_name=region)
        self.s3 = boto3.client('s3')
        self.region = region
    def list_instances(self):
        resp = self.ec2.describe_instances()
        instances = []
        for reservation in resp['Reservations']:
            for instance in reservation['Instances']:
                instances.append({
                    'Id': instance['InstanceId'],
                    'Type': instance['InstanceType'],
                    'State': instance['State']['Name'],
                    'Name': next((tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name'), '')
                })
        return instances
    def start_instance(self, instance_id):
        self.ec2.start_instances(InstanceIds=[instance_id])
        print(f"Starting {instance_id}")
    def stop_instance(self, instance_id):
        self.ec2.stop_instances(InstanceIds=[instance_id])
        print(f"Stopping {instance_id}")
    def tag_instance(self, instance_id, key, value):
        self.ec2.create_tags(Resources=[instance_id], Tags=[{'Key': key, 'Value': value}])
        print(f"Tagged {instance_id} with {key}={value}")

    def launch_instance(self, ami, instance_type='t2.micro', key_name=None, security_group_ids=None):
        params = {
            'ImageId': ami,
            'InstanceType': instance_type,
            'MinCount': 1,
            'MaxCount': 1
        }
        if key_name:
            params['KeyName'] = key_name
        if security_group_ids:
            params['SecurityGroupIds'] = security_group_ids
        resp = self.ec2.run_instances(**params)
        instance_id = resp['Instances'][0]['InstanceId']
        print(f"Launched instance {instance_id}")
        return instance_id