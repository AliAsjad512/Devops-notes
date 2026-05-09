import psycopg2
import argparse
import json
from datetime import datetime

class PGPerformance:
    def __init__(self, host, port, user, password, database):
        self.conn = psycopg2.connect(host=host, port=port, user=user, password=password, database=database)

   def get_top_slow_queries(self, limit=10):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT query, mean_time, calls, total_time
            FROM pg_stat_statements
            ORDER BY mean_time DESC
            LIMIT %s
        """, (limit,))
        rows = cur.fetchall()
        return [{'query': r[0][:200], 'mean_time_ms': round(r[1], 2), 'calls': r[2], 'total_time_sec': round(r[3] / 1000, 2)} for r in rows]
   def get_cache_hit_ratio(self):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT
                sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) * 100 as hit_ratio
            FROM pg_statio_user_tables
        """)
        return cur.fetchone()[0]
