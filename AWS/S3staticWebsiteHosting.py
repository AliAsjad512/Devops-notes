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

 s3.put_bucket_website(
        Bucket=bucket_name,
        WebsiteConfiguration={
            'IndexDocument': {'Suffix': index_file},
            'ErrorDocument': {'Key': 'error.html'}
        }
    )
    print("Static website hosting enabled.")

policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": f"arn:aws:s3:::{bucket_name}/*"
        }]
    }
    s3.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(policy))
    print("Bucket policy set to public read.")
