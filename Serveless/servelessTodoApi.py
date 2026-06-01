import json
import boto3
import os
from uuid import uuid4
from datetime import datetime
dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)