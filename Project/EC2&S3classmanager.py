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
    def list_buckets(self):
        buckets = self.s3.list_buckets().get('Buckets', [])
        return [b['Name'] for b in buckets]

    def create_bucket(self, bucket_name):
        if self.region == 'us-east-1':
            self.s3.create_bucket(Bucket=bucket_name)
        else:
            self.s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': self.region})
        print(f"Bucket {bucket_name} created")

    def delete_bucket(self, bucket_name):
        # Delete all objects first (simple version)
        objects = self.s3.list_objects_v2(Bucket=bucket_name).get('Contents', [])
        for obj in objects:
            self.s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
        self.s3.delete_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} deleted")

    def main():
    parser = argparse.ArgumentParser(description='AWS EC2 & S3 Manager')
    parser.add_argument('--region', default='us-east-1')
    subparsers = parser.add_subparsers(dest='command', required=True)

    # EC2 commands
    ec2_parser = subparsers.add_parser('ec2-list')
    ec2_start = subparsers.add_parser('ec2-start')
    ec2_start.add_argument('instance_id')
    ec2_stop = subparsers.add_parser('ec2-stop')
    ec2_stop.add_argument('instance_id')
    ec2_tag = subparsers.add_parser('ec2-tag')
    ec2_tag.add_argument('instance_id')
    ec2_tag.add_argument('key')
    ec2_tag.add_argument('value')
    ec2_launch = subparsers.add_parser('ec2-launch')
    ec2_launch.add_argument('--ami', required=True)
    ec2_launch.add_argument('--type', default='t2.micro')
    ec2_launch.add_argument('--key', help='Key pair name')
    ec2_launch.add_argument('--sg', nargs='+', help='Security group IDs')

    # S3 commands
    s3_list = subparsers.add_parser('s3-list')
    s3_create = subparsers.add_parser('s3-create')
    s3_create.add_argument('bucket')
    s3_delete = subparsers.add_parser('s3-delete')
    s3_delete.add_argument('bucket')

    args = parser.parse_args()
    aws = AWSManager(args.region)

    if args.command == 'ec2-list':
        for inst in aws.list_instances():
            print(f"{inst['Id']} [{inst['State']}] {inst['Name']} ({inst['Type']})")
    elif args.command == 'ec2-start':
        aws.start_instance(args.instance_id)
    elif args.command == 'ec2-stop':
        aws.stop_instance(args.instance_id)
    elif args.command == 'ec2-tag':
        aws.tag_instance(args.instance_id, args.key, args.value)
    elif args.command == 'ec2-launch':
        aws.launch_instance(args.ami, args.type, args.key, args.sg)
    elif args.command == 's3-list':
        for b in aws.list_buckets():
            print(b)
    elif args.command == 's3-create':
        aws.create_bucket(args.bucket)
    elif args.command == 's3-delete':
        aws.delete_bucket(args.bucket)

if __name__ == '__main__':
    main()