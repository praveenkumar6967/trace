#!/usr/bin/env python3
"""
TRACE × X — Cloud Database Migration Utility
Department of Computer Science & Engineering | T.J.S. Engineering College

Migrates local SQLite database (tracex.db) to persistent cloud database (Turso / LibSQL).
Preserves all existing user records, event states, case evidence, 450 question answer keys,
and administrator credentials with full verification before and after migration.

Usage:
    python migrate_to_cloud.py [--dry-run]
"""

import os
import sys
import sqlite3
import argparse

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LOCAL_DB_PATH = os.environ.get('TRACEX_DB_PATH', os.path.join(ROOT_DIR, 'tracex.db'))

TABLES_TO_MIGRATE = [
    'admins',
    'admin_sessions',
    'teams',
    'sessions',
    'violations',
    'submissions',
    'event_state',
    'audit_logs',
    'event_reports',
    'event_report_versions',
    'cases',
    'questions',
    'backups',
    'export_logs',
    'round_timers',
    'team_sessions',
    'score_audit_logs'
]

def main():
    parser = argparse.ArgumentParser(description="TRACE × X Cloud Database Migration Tool")
    parser.add_argument('--dry-run', action='store_true', help="Inspect local records without writing to remote database")
    args = parser.parse_args()

    print("=" * 70)
    print("TRACE × X — AUTHORITATIVE CLOUD DATABASE MIGRATION ENGINE")
    print("Department of Computer Science & Engineering | T.J.S. Engineering College")
    print("=" * 70)

    if not os.path.exists(LOCAL_DB_PATH):
        print(f"[ERROR] Source database '{LOCAL_DB_PATH}' not found.")
        sys.exit(1)

    # 1. Connect to local database (read-only mode)
    local_conn = sqlite3.connect(f"file:{os.path.abspath(LOCAL_DB_PATH)}?mode=ro", uri=True)
    local_conn.row_factory = sqlite3.Row
    local_cur = local_conn.cursor()

    local_cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    existing_tables = {r[0] for r in local_cur.fetchall()}

    print(f"\n[PHASE 1] Inspected Local Database: {LOCAL_DB_PATH}")
    local_counts = {}
    for tbl in TABLES_TO_MIGRATE:
        if tbl in existing_tables:
            local_cur.execute(f"SELECT COUNT(*) as cnt FROM {tbl}")
            cnt = local_cur.fetchone()['cnt']
            local_counts[tbl] = cnt
            print(f"  • {tbl.ljust(25)} : {cnt} records")
        else:
            print(f"  • {tbl.ljust(25)} : [TABLE NOT PRESENT LOCALLY]")

    if args.dry_run:
        print("\n[INFO] Dry-run completed. No remote writes performed.")
        local_conn.close()
        return

    # 2. Check remote database credentials
    turso_url = os.environ.get('TURSO_DATABASE_URL') or os.environ.get('LIBSQL_URL')
    turso_token = os.environ.get('TURSO_AUTH_TOKEN') or os.environ.get('LIBSQL_AUTH_TOKEN')

    if not turso_url or not turso_token:
        print("\n[NOTICE] Remote Cloud Database credentials not found in environment:")
        print("  To migrate to Turso / LibSQL, set the following environment variables:")
        print("    TURSO_DATABASE_URL = 'libsql://your-db-org.turso.io'")
        print("    TURSO_AUTH_TOKEN    = 'your-turso-jwt-token'")
        print("\nAlternatively, run in dry-run mode: python migrate_to_cloud.py --dry-run")
        local_conn.close()
        return

    try:
        import libsql_experimental as libsql
    except ImportError:
        print("\n[ERROR] 'libsql-experimental' package is required for Turso migration.")
        print("Install via: pip install libsql-experimental")
        local_conn.close()
        sys.exit(1)

    print(f"\n[PHASE 2] Connecting to Remote Cloud Database: {turso_url}")
    remote_conn = libsql.connect(turso_url, auth_token=turso_token)
    remote_cur = remote_conn.cursor()

    # 3. Create tables and migrate schema & rows
    print("\n[PHASE 3] Migrating Tables & Data...")
    for tbl in TABLES_TO_MIGRATE:
        if tbl not in existing_tables:
            continue

        # Get table creation SQL
        local_cur.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name = ?", (tbl,))
        create_sql_row = local_cur.fetchone()
        if not create_sql_row or not create_sql_row['sql']:
            continue

        create_sql = create_sql_row['sql']
        remote_cur.execute(create_sql)

        # Get columns
        local_cur.execute(f"PRAGMA table_info({tbl})")
        cols = [c['name'] for c in local_cur.fetchall()]
        col_names = ', '.join(cols)
        placeholders = ', '.join(['?'] * len(cols))

        local_cur.execute(f"SELECT * FROM {tbl}")
        rows = local_cur.fetchall()
        
        insert_sql = f"INSERT OR REPLACE INTO {tbl} ({col_names}) VALUES ({placeholders})"
        for r in rows:
            remote_cur.execute(insert_sql, tuple(r))

        remote_conn.commit()
        print(f"  ✓ {tbl.ljust(25)} : {len(rows)} records synchronized")

    # 4. Verify record counts
    print("\n[PHASE 4] Verifying Row Count Parity...")
    all_match = True
    for tbl, l_cnt in local_counts.items():
        remote_cur.execute(f"SELECT COUNT(*) as cnt FROM {tbl}")
        r_cnt = remote_cur.fetchone()[0]
        match = (l_cnt == r_cnt)
        status = "MATCH" if match else "MISMATCH"
        print(f"  [{status}] {tbl.ljust(25)} : Local={l_cnt}, Remote={r_cnt}")
        if not match:
            all_match = False

    remote_conn.close()
    local_conn.close()

    if all_match:
        print("\n[SUCCESS] Cloud database migration complete! All records verified.")
    else:
        print("\n[WARNING] Discrepancies detected between local and remote datasets.")

if __name__ == '__main__':
    main()
