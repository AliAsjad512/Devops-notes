import boto3
import json
import os

sqs = boto3.client('sqs')
sns = boto3.client('sns')
dlq_url = os.environ['DLQ_URL']
sns_topic = os.environ.get('SNS_TOPIC_ARN', '')
