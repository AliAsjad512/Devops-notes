import subprocess
import boto3
import argparse
import os
import gzip
import datetime
import tempfile
from cryptography.fernet import Fernet