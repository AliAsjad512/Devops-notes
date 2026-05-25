import subprocess
import argparse
import sys
import os
import json
class TerraformWrapper:
    def __init__(self, working_dir='.'):
        self.working_dir = working_dir