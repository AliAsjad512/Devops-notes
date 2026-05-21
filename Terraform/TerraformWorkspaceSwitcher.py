import subprocess
import argparse
import sys
import re
class TerraformWorkspace:
    def __init__(self, tf_dir='.'):
        self.tf_dir = tf_dir
