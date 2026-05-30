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
