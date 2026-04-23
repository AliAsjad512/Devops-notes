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
    def find_unused_images(self, days_old=30):
        cutoff = datetime.datetime.now() - datetime.timedelta(days=days_old)
        images = self.list_images()
        unused = []
        for img in images:
            if img['used_by_containers']:
                continue
            if img['created'] < cutoff and not any(t != '<none>:<none>' for t in img['tags']):
                unused.append(img)
        return unused