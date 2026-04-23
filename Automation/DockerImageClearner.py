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
    def delete_old_images(self, days_old=30, dry_run=True):
        to_delete = self.find_unused_images(days_old)
        for img in to_delete:
            if dry_run:
                print(f"[DRY RUN] Would delete: {img['id']} (created {img['created']})")
            else:
                try:
                    self.client.images.remove(img['id'], force=True)
                    print(f"✅ Deleted: {img['id']}")
                except Exception as e:
                    print(f"❌ Failed to delete {img['id']}: {e}")
        return len(to_delete)
    def delete_untagged(self, dry_run=True):
        images = self.client.images.list(filters={'dangling': True})
        for img in images:
            if dry_run:
                print(f"[DRY RUN] Would delete untagged: {img.id[:12]}")
            else:
                self.client.images.remove(img.id)
                print(f"✅ Deleted untagged: {img.id[:12]}")
        return len(images)
    
    if __name__ == '__main__':
     parser = argparse.ArgumentParser(description='Docker Image Cleaner')
    parser.add_argument('--days', type=int, default=30, help='Age in days')
    parser.add_argument('--dry-run', action='store_true', help='Preview without deleting')
    parser.add_argument('--untagged-only', action='store_true', help='Delete only untagged images')
    parser.add_argument('--all-unused', action='store_true', help='Delete all unused images older than days')
    args = parser.parse_args()

    cleaner = DockerImageCleaner()
    if args.untagged_only:
        count = cleaner.delete_untagged(args.dry_run)
        print(f"Deleted {count} untagged images")
    elif args.all_unused:
        count = cleaner.delete_old_images(args.days, args.dry_run)
        print(f"Deleted {count} old/unused images")
    else:
        parser.print_help()