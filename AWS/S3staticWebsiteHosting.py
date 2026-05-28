import boto3
import argparse
def create_static_website(bucket_name, region='us-east-1', index_file='index.html', content=None):
    s3 = boto3.client('s3', region_name=region)

    # 1. Create bucket
    if region == 'us-east-1':
        s3.create_bucket(Bucket=bucket_name)
    else:
        s3.create_bucket(Bucket=bucket_name,
                         CreateBucketConfiguration={'LocationConstraint': region})
    print(f"Bucket '{bucket_name}' created.")
