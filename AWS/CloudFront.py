import boto3
import argparse
import time

class CloudFrontInvalidator:
    def __init__(self, distribution_id):
        self.cf = boto3.client('cloudfront')
        self.dist_id = distribution_id
    def invalidate(self, paths=['/*'], wait=False):
        """Invalidate paths (default: everything)."""
        response = self.cf.create_invalidation(
            DistributionId=self.dist_id,
            InvalidationBatch={
                'Paths': {'Quantity': len(paths), 'Items': paths},
                'CallerReference': str(int(time.time()))
            }
        )
        invalidation_id = response['Invalidation']['Id']
        print(f"Invalidation {invalidation_id} started")
        if wait:
            self._wait(invalidation_id)
        return invalidation_id
    def _wait(self, inval_id):
        while True:
            status = self.cf.get_invalidation(DistributionId=self.dist_id, Id=inval_id)
            if status['Invalidation']['Status'] == 'Completed':
                print("Invalidation completed")
                break
            time.sleep(3)