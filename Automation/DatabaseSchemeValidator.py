import argparse
import json
import psycopg2
import pymysql
from deepdiff import DeepDiff
 
 class SchemaValidator:
    def __init__(self, db_type, host, port, user, password, database):
        self.db_type = db_type
        self.conn = self._connect(host, port, user, password, database)
