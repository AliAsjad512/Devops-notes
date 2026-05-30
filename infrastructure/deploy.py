import boto3
import zipfile
import os
import json
import time
def create_word_counter_stack(bucket_name, function_name, topic_name):
    iam = boto3.client('iam')
    lambda_client = boto3.client('lambda')
    s3 = boto3.client('s3')
    sns = boto3.client('sns')
    topic = sns.create_topic(Name=topic_name)
    topic_arn = topic['TopicArn']
    print(f"SNS topic created: {topic_arn}")

    # (Optional) Add your email subscription
    response = input(f"Enter email to subscribe to {topic_name} (or press Enter to skip): ")
    if response:
        sns.subscribe(TopicArn=topic_arn, Protocol='email', Endpoint=response)
        print(f"Subscription request sent to {response}. Confirm via email.")
     assume_role_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "lambda.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    }
    role_name = f"{function_name}_role"
    role = iam.create_role(RoleName=role_name, AssumeRolePolicyDocument=json.dumps(assume_role_policy))
    # Attach policies
    iam.attach_role_policy(RoleName=role_name, PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole')
    iam.attach_role_policy(RoleName=role_name, PolicyArn='arn:aws:iam::aws:policy/AmazonSNSFullAccess')
    iam.attach_role_policy(RoleName=role_name, PolicyArn='arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess')
