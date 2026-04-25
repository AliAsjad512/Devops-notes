import subprocess
import argparse
import re
from datetime import datetime, timedelta
class ReleaseNotesGenerator:
    def __init__(self, repo_path='.'):
        self.repo_path = repo_path