import boto3
import argparse
import datetime
from collections import defaultdict

class EBSSnapshotScheduler:
    def __init__(self, region='us-east-1'):
        self.ec2 = boto3.client('ec2', region_name=region)
        self.region = region

    def get_volumes(self, volume_ids=None, tag_filter=None):
        filters = []
        if volume_ids:
            return [self.ec2.describe_volumes(VolumeIds=volume_ids)['Volumes'][0]]
        if tag_filter:
            key, value = tag_filter.split('=')
            filters.append({'Name': f'tag:{key}', 'Values': [value]})
        response = self.ec2.describe_volumes(Filters=filters)
        return response['Volumes']
    def create_snapshot(self, volume_id, description=None):
        desc = description or f"Automated snapshot at {datetime.datetime.utcnow().isoformat()}"
        snapshot = self.ec2.create_snapshot(VolumeId=volume_id, Description=desc)
        print(f"✅ Creating snapshot {snapshot['SnapshotId']} for volume {volume_id}")
        return snapshot['SnapshotId']
    def create_snapshots_for_all(self, volume_ids=None, tag_filter=None):
        volumes = self.get_volumes(volume_ids, tag_filter)
        snapshots = []
        for vol in volumes:
            snap_id = self.create_snapshot(vol['VolumeId'])
            # Add retention tag
            retention_date = (datetime.datetime.now() + datetime.timedelta(days=30)).isoformat()
            self.ec2.create_tags(Resources=[snap_id], Tags=[{'Key': 'DeleteAfter', 'Value': retention_date}])
            snapshots.append(snap_id)
        return snapshots

