import boto3
import json
import os

sqs = boto3.client('sqs')
sns = boto3.client('sns')
dlq_url = os.environ['DLQ_URL']
sns_topic = os.environ.get('SNS_TOPIC_ARN', '')

def lambda_handler(event, context):
    messages = event['Records']
    failures = []

    for msg in messages:
        body = msg['body']
        # Process the dead letter (e.g., log to CloudWatch, send to S3, etc.)
        print(f"DLQ message: {body}")
        # Optionally send SNS alert
        if sns_topic:
            sns.publish(TopicArn=sns_topic, Message=f"DLQ message received: {body[:200]}", Subject="DLQ Alert")
 # Delete from DLQ after processing
        receipt = msg['receiptHandle']
        sqs.delete_message(QueueUrl=dlq_url, ReceiptHandle=receipt)
    return {'statusCode': 200, 'processed': len(messages)}