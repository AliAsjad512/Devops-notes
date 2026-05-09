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

    def get_blocking_locks(self):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT
                blocked_locks.pid AS blocked_pid,
                blocked_activity.query AS blocked_query,
                blocking_locks.pid AS blocking_pid,
                blocking_activity.query AS blocking_query
            FROM pg_locks blocked_locks
            JOIN pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
            JOIN pg_locks blocking_locks ON blocking_locks.locktype = blocked_locks.locktype
                AND blocking_locks.database IS NOT DISTINCT FROM blocked_locks.database
                AND blocking_locks.relation IS NOT DISTINCT FROM blocked_locks.relation
                AND blocking_locks.page IS NOT DISTINCT FROM blocked_locks.page
                AND blocking_locks.tuple IS NOT DISTINCT FROM blocked_locks.tuple
                AND blocking_locks.virtualxid IS NOT DISTINCT FROM blocked_locks.virtualxid
                AND blocking_locks.transactionid IS NOT DISTINCT FROM blocked_locks.transactionid
                AND blocking_locks.classid IS NOT DISTINCT FROM blocked_locks.classid
                AND blocking_locks.objid IS NOT DISTINCT FROM blocked_locks.objid
                AND blocking_locks.objsubid IS NOT DISTINCT FROM blocked_locks.objsubid
                AND blocking_locks.pid != blocked_locks.pid
            JOIN pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
            WHERE NOT blocked_locks.granted
        """)
        return cur.fetchall()
    def generate_report(self):
        return {
            'timestamp': datetime.utcnow().isoformat(),
            'cache_hit_ratio': self.get_cache_hit_ratio(),
            'top_slow_queries': self.get_top_slow_queries(),
            'blocking_locks': self.get_blocking_locks()
        }
