import docker
import argparse
import time
import gzip
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

class DockerLogCollector:
    def __init__(self):
        self.client = docker.from_env()