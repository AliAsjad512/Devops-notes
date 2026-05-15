import subprocess
import argparse
import sys
import json
from pathlib import Path
 class PulumiManager:
    def __init__(self, stack_name, work_dir='.'):
        self.stack_name = stack_name
        self.work_dir = Path(work_dir)
