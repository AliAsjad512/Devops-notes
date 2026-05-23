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