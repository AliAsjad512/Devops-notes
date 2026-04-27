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
        
    def get_schema_postgres(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT table_name, column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_schema = 'public'
            ORDER BY table_name, ordinal_position
        """)
        schema = {}
        for row in cursor.fetchall():
            table, col, dtype, nullable = row
            if table not in schema:
                schema[table] = []
            schema[table].append({
                'column': col,
                'type': dtype,
                'nullable': nullable == 'YES'
            })
        return schema
    
    def get_schema_mysql(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT table_name, column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_schema = DATABASE()
            ORDER BY table_name, ordinal_position
        """)
        schema = {}
        for row in cursor.fetchall():
            table, col, dtype, nullable = row
            if table not in schema:
                schema[table] = []
            schema[table].append({
                'column': col,
                'type': dtype,
                'nullable': nullable == 'YES'
            })
        return schema
    
     def get_schema(self):
        if self.db_type == 'postgres':
            return self.get_schema_postgres()
        else:
            return self.get_schema_mysql()

    def compare_schemas(self, schema1, schema2):
        diff = DeepDiff(schema1, schema2, ignore_order=True)
        return diff

