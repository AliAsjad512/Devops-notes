import boto3
import argparse
import time
import sys

class RDSBackupCopier:
    def __init__(self, source_region, target_region):
        self.source = boto3.client('rds', region_name=source_region)
        self.target = boto3.client('rds', region_name=target_region)
        self.source_region = source_region
        self.target_region = target_region
    def list_snapshots(self, days_back=7):
        """List manual snapshots created in the last N days."""
        import datetime
        cutoff = datetime.datetime.now() - datetime.timedelta(days=days_back)
        snapshots = self.source.describe_db_snapshots(SnapshotType='manual')['DBSnapshots']
        recent = [s for s in snapshots if s['SnapshotCreateTime'].replace(tzinfo=None) > cutoff]
        return recent
    def copy_snapshot(self, snapshot_id, target_snapshot_id):
        """Copy a snapshot to the target region."""
        try:
            response = self.target.copy_db_snapshot(
                SourceDBSnapshotIdentifier=f'arn:aws:rds:{self.source_region}:{self.get_account_id()}:snapshot:{snapshot_id}',
                TargetDBSnapshotIdentifier=target_snapshot_id,
                CopyTags=True
            )
            print(f"Copy initiated: {target_snapshot_id}")
            return response['DBSnapshot']['DBSnapshotArn']
        except Exception as e:
            print(f"Error copying {snapshot_id}: {e}")
            return None
        def get_account_id(self):
        sts = boto3.client('sts')
        return sts.get_caller_identity()['Account']
    
      def run(self, days_back=7, dry_run=True):
        snapshots = self.list_snapshots(days_back)
        print(f"Found {len(snapshots)} snapshots from the last {days_back} days")
        for snap in snapshots:
            source_id = snap['DBSnapshotIdentifier']
            target_id = f"{source_id}-copy"
            if dry_run:
                print(f"[DRY RUN] Would copy {source_id} to {self.target_region}:{target_id}")
            else:
                self.copy_snapshot(source_id, target_id)
                time.sleep(1)  # avoid rate limits
