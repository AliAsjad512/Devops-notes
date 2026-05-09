import psycopg2
import argparse
import json
from datetime import datetime

class PGPerformance:
    def __init__(self, host, port, user, password, database):
        self.conn = psycopg2.connect(host=host, port=port, user=user, password=password, database=database)