import argparse
import requests
import json

 class NomadMonitor:
    def __init__(self, addr='http://localhost:4646'):
        self.addr = addr.rstrip('/')