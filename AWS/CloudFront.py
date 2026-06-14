import boto3
import argparse
import time

class CloudFrontInvalidator:
    def __init__(self, distribution_id):
        self.cf = boto3.client('cloudfront')
        self.dist_id = distribution_id