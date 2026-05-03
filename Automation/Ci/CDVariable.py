import os
import sys
import argparse
import re

class EnvValidator:
    def __init__(self, required_vars=None, patterns=None):
        self.required_vars = required_vars or []
        self.patterns = patterns or {}
    def add_required(self, var_name):
        self.required_vars.append(var_name)
    def add_pattern(self, var_name, regex):
        self.patterns[var_name] = regex



