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

     time.sleep(10)

    # 3. Package Lambda code
    with zipfile.ZipFile('lambda.zip', 'w') as z:
        z.write('lambda_function.py')

    with open('lambda.zip', 'rb') as f:
        zip_data = f.read()
   # 4. Create Lambda function
    lambda_client.create_function(
        FunctionName=function_name,
        Runtime='python3.9',
        Role=role['Role']['Arn'],
        Handler='lambda_function.lambda_handler',
        Code={'ZipFile': zip_data},
        Environment={'Variables': {'SNS_TOPIC_ARN': topic_arn}}
    )
    print(f"Lambda function '{function_name}' created.")

    # 5. Create S3 bucket for file uploads
    s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'us-east-1'})
    print(f"S3 bucket '{bucket_name}' created.")

    # 6. Add S3 bucket notification to trigger Lambda
    lambda_arn = lambda_client.get_function(FunctionName=function_name)['Configuration']['FunctionArn']
    # Grant S3 invoke permission
    lambda_client.add_permission(
        FunctionName=function_name,
        StatementId='s3invoke',
        Action='lambda:InvokeFunction',
        Principal='s3.amazonaws.com',
        SourceArn=f'arn:aws:s3:::{bucket_name}'
    )
    notification = {
        'LambdaFunctionConfigurations': [{
            'Id': 'word-counter-trigger',
            'LambdaFunctionArn': lambda_arn,
            'Events': ['s3:ObjectCreated:*']
        }]
    }
    s3.put_bucket_notification_configuration(Bucket=bucket_name, NotificationConfiguration=notification)
    print("S3 event notification configured.")

    print("\n✅ Deployment complete!")
    print(f"Upload a .txt file to s3://{bucket_name} to trigger the word counter.")
    print(f"You will receive an email (if subscribed) with the word count.")
