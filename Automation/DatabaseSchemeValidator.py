import argparse
import json
import psycopg2
import pymysql
from deepdiff import DeepDiff
 
 class SchemaValidator:
    def __init__(self, db_type, host, port, user, password, database):
        self.db_type = db_type
        self.conn = self._connect(host, port, user, password, database)
    def _connect(self, host, port, user, password, database):
        if self.db_type == 'postgres':
            return psycopg2.connect(host=host, port=port, user=user, password=password, database=database)
        else:
            return pymysql.connect(host=host, port=port, user=user, password=password, database=database)

