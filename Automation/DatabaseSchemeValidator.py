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
    

    if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Schema Migration Validator')
    parser.add_argument('--db-type', choices=['postgres', 'mysql'], required=True)
    parser.add_argument('--host1', required=True)
    parser.add_argument('--port1', type=int, required=True)
    parser.add_argument('--user1', required=True)
    parser.add_argument('--password1', required=True)
    parser.add_argument('--database1', required=True)
    parser.add_argument('--host2', required=True)
    parser.add_argument('--port2', type=int, required=True)
    parser.add_argument('--user2', required=True)
    parser.add_argument('--password2', required=True)
    parser.add_argument('--database2', required=True)
    args = parser.parse_args()

    v1 = SchemaValidator(args.db_type, args.host1, args.port1, args.user1, args.password1, args.database1)
    v2 = SchemaValidator(args.db_type, args.host2, args.port2, args.user2, args.password2, args.database2)

    schema1 = v1.get_schema()
    schema2 = v2.get_schema()
    diff = v1.compare_schemas(schema1, schema2)

    if diff:
        print("❌ Schema differences found:")
        print(json.dumps(diff, indent=2, default=str))
    else:
        print("✅ Schemas are identical")

