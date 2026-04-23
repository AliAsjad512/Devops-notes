import docker
import argparse
import datetime
from collections import defaultdict
class DockerImageCleaner:
    def __init__(self):
        self.client = docker.from_env()

    def list_images(self):
        images = self.client.images.list(all=True)
        img_data = []
        for img in images:
            tags = img.tags
            if not tags:
                tags = ['<none>:<none>']
            img_data.append({
                'id': img.id[:12],
                'tags': tags,
                'size': img.attrs['Size'],
                'created': datetime.datetime.fromtimestamp(img.attrs['Created']),
                'used_by_containers': len(img.attrs.get('ContainerConfig', {}).get('Hostname', [])) > 0
            })
        return img_data
