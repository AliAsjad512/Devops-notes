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