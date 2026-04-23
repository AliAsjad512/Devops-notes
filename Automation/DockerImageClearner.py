import docker
import argparse
import datetime
from collections import defaultdict
class DockerImageCleaner:
    def __init__(self):
        self.client = docker.from_env()
