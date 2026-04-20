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