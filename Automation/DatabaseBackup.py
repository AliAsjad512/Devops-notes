import subprocess
import boto3
import argparse
import os
import gzip
import datetime
import tempfile
from cryptography.fernet import Fernet
class DatabaseBackup:
    def __init__(self, db_type, host, port, user, password, database, s3_bucket, s3_prefix='backups/'):
        self.db_type = db_type
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.s3 = boto3.client('s3')
        self.s3_bucket = s3_bucket
        self.s3_prefix = s3_prefix.rstrip('/') + '/'
    def dump_postgres(self):
        """Dump PostgreSQL database"""
        env = os.environ.copy()
        env['PGPASSWORD'] = self.password
        cmd = [
            'pg_dump',
            '-h', self.host,
            '-p', str(self.port),
            '-U', self.user,
            '-d', self.database,
            '-F', 'c',  # custom format
            '-f', '-'
        ]
        result = subprocess.run(cmd, capture_output=True, text=False, env=env)
        if result.returncode != 0:
            raise Exception(f"pg_dump failed: {result.stderr}")
        return result.stdout
    def dump_mysql(self):
        """Dump MySQL database"""
        cmd = [
            'mysqldump',
            '-h', self.host,
            '-P', str(self.port),
            '-u', self.user,
            f'-p{self.password}',
            self.database,
            '--single-transaction',
            '--compress'
        ]
        result = subprocess.run(cmd, capture_output=True, text=False)
        if result.returncode != 0:
            raise Exception(f"mysqldump failed: {result.stderr}")
        return result.stdout
    
    def encrypt_data(self, data, key):
        """Encrypt backup data with Fernet"""
        f = Fernet(key)
        return f.encrypt(data)

    def compress_data(self, data):
        """Gzip compress data"""
        return gzip.compress(data)

    def upload_to_s3(self, data, filename):
        
        self.s3.put_object(Bucket=self.s3_bucket, Key=self.s3_prefix + filename, Body=data)
        print(f"✅ Uploaded {filename} to s3://{self.s3_bucket}/{self.s3_prefix}{filename}")

    def create_backup(self, encrypt_key=None):
        
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{self.database}_{timestamp}.dump"

        # Dump database
        print(f"📦 Dumping {self.db_type} database {self.database}...")
        if self.db_type == 'postgres':
            dump_data = self.dump_postgres()
        else:
            dump_data = self.dump_mysql()

        # Compress
        compressed = self.compress_data(dump_data)
        filename_gz = filename + '.gz'

        # Encrypt if key provided
        if encrypt_key:
            encrypted = self.encrypt_data(compressed, encrypt_key)
            final_data = encrypted
            filename_final = filename_gz + '.enc'
        else:
            final_data = compressed
            filename_final = filename_gz

        # Upload
        self.upload_to_s3(final_data, filename_final)
        print(f"✅ Backup complete: {filename_final}")
        return filename_final
    def list_backups(self):
        
        response = self.s3.list_objects_v2(Bucket=self.s3_bucket, Prefix=self.s3_prefix)
        if 'Contents' not in response:
            return []
        return [obj['Key'] for obj in response['Contents']]

    def delete_old_backups(self, days=30):
        """Delete backups older than N days"""
        cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)
        deleted = []
        response = self.s3.list_objects_v2(Bucket=self.s3_bucket, Prefix=self.s3_prefix)
        if 'Contents' in response:
            for obj in response['Contents']:
                if obj['LastModified'] < cutoff:
                    self.s3.delete_object(Bucket=self.s3_bucket, Key=obj['Key'])
                    deleted.append(obj['Key'])
        print(f"🗑️ Deleted {len(deleted)} old backups")
        return deleted
    
    if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Database Backup to S3')
    parser.add_argument('--db-type', choices=['postgres', 'mysql'], required=True)
    parser.add_argument('--host', required=True)
    parser.add_argument('--port', type=int, required=True)
    parser.add_argument('--user', required=True)
    parser.add_argument('--password', required=True)
    parser.add_argument('--database', required=True)
    parser.add_argument('--s3-bucket', required=True)
    parser.add_argument('--s3-prefix', default='backups/')
    parser.add_argument('--encrypt-key', help='Fernet encryption key')
    parser.add_argument('--action', choices=['backup', 'list', 'cleanup'], default='backup')
    parser.add_argument('--days', type=int, default=30)
    args = parser.parse_args()

    backup = DatabaseBackup(args.db_type, args.host, args.port, args.user, args.password,
                            args.database, args.s3_bucket, args.s3_prefix)
    if args.action == 'backup':
        backup.create_backup(args.encrypt_key)
    elif args.action == 'list':
        backups = backup.list_backups()
        print(f"Backups in s3://{args.s3_bucket}/{args.s3_prefix}:")
        for b in backups:
            print(f"  - {b}")
    elif args.action == 'cleanup':
        backup.delete_old_backups(args.days)
