import boto3
import argparse
import datetime
import time
class BackupManager:
    def __init__(self, region='us-east-1'):
        self.ec2 = boto3.client('ec2', region_name=region)

    def create_snapshots(self, tag_key='Backup', tag_value='true', dry_run=True):
        instances = self.ec2.describe_instances(Filters=[
            {'Name': f'tag:{tag_key}', 'Values': [tag_value]},
            {'Name': 'instance-state-name', 'Values': ['running']}
        ])
        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                description = f"Backup {instance_id} {datetime.datetime.now().isoformat()}"
                if dry_run:
                    print(f"[DRY RUN] Would snapshot {instance_id}")
                else:
                    snap = self.ec2.create_snapshot(VolumeId=instance['BlockDeviceMappings'][0]['Ebs']['VolumeId'], Description=description)
                    # Tag snapshot
                    self.ec2.create_tags(Resources=[snap['SnapshotId']], Tags=[{'Key': 'Backup', 'Value': 'true'}])
                    print(f"Snapshot {snap['SnapshotId']} for {instance_id}")

    def delete_old_snapshots(self, retention_days=30, dry_run=True):
        cutoff = datetime.datetime.now() - datetime.timedelta(days=retention_days)
        snapshots = self.ec2.describe_snapshots(OwnerIds=['self'])['Snapshots']
        for snap in snapshots:
            if snap['StartTime'].replace(tzinfo=None) < cutoff:
                if dry_run:
                    print(f"[DRY RUN] Would delete {snap['SnapshotId']}")
                else:
                    self.ec2.delete_snapshot(SnapshotId=snap['SnapshotId'])
                    print(f"Deleted {snap['SnapshotId']}")



        if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--action', choices=['create', 'cleanup'], required=True)
    parser.add_argument('--retention-days', type=int, default=30)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    mgr = BackupManager()
    if args.action == 'create':
        mgr.create_snapshots(dry_run=args.dry_run)
    else:
        mgr.delete_old_snapshots(args.retention_days, args.dry_run)

