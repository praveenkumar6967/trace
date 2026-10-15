"""
TRACE × X — Backend Server & SQLite Database
Department of Computer Science & Engineering | T.J.S. Engineering College
Authoritative backend for Admin Authentication, Event Control, Team Registry,
Live Sessions, Security Violations, Answer Evaluation, and Audit Logging.
"""

import os
import sys
import json
import sqlite3
import hashlib
import secrets
import time
import csv
import io
import shutil
from urllib.parse import urlparse, parse_qs
from http.server import SimpleHTTPRequestHandler, HTTPServer

PORT = 3000
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
IS_VERCEL = bool(os.environ.get('VERCEL') or os.environ.get('VERCEL_ENV') or os.environ.get('AWS_LAMBDA_FUNCTION_NAME'))

if IS_VERCEL:
    DB_FILE = os.environ.get('TRACEX_DB_PATH', '/tmp/tracex.db')
    BACKUP_DIR = os.environ.get('TRACEX_BACKUP_DIR', '/tmp/backups')
    bundled_db = os.path.join(ROOT_DIR, 'tracex.db')
    if not os.path.exists(DB_FILE) and os.path.exists(bundled_db):
        try:
            shutil.copyfile(bundled_db, DB_FILE)
        except Exception as e:
            print(f"[TRACE × X] Warning: could not copy bundled db to /tmp: {e}")
else:
    DB_FILE = os.environ.get('TRACEX_DB_PATH', os.environ.get('SQLITE_DB_PATH', os.path.join(ROOT_DIR, 'tracex.db')))
    BACKUP_DIR = os.environ.get('TRACEX_BACKUP_DIR', os.path.join(ROOT_DIR, 'backups'))

try:
    os.makedirs(BACKUP_DIR, exist_ok=True)
except Exception:
    pass

# -----------------------------------------------------------------------------
# Database Setup & Schema
# -----------------------------------------------------------------------------
def get_db():
    # 1. Check for Turso / LibSQL Cloud Database configuration
    turso_url = os.environ.get('TURSO_DATABASE_URL') or os.environ.get('LIBSQL_URL')
    turso_token = os.environ.get('TURSO_AUTH_TOKEN') or os.environ.get('LIBSQL_AUTH_TOKEN')
    if turso_url and turso_token:
        try:
            import libsql_experimental as libsql
            conn = libsql.connect(turso_url, auth_token=turso_token)
            conn.row_factory = sqlite3.Row
            return conn
        except Exception as e:
            print(f"[TRACE × X] Turso connection note: {e}. Falling back to SQLite.")

    # 2. Local / Serverless SQLite
    active_db = os.environ.get('TRACEX_DB_PATH', os.environ.get('SQLITE_DB_PATH', DB_FILE))
    parent = os.path.dirname(active_db)
    if parent:
        try:
            os.makedirs(parent, exist_ok=True)
        except Exception:
            pass
    conn = sqlite3.connect(active_db, timeout=15.0)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA journal_mode = WAL")
        conn.execute("PRAGMA busy_timeout = 15000")
    except:
        pass
    return conn

def hash_password(password, salt=None):
    if not salt:
        salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000).hex()
    return hashed, salt

def verify_password(password, stored_hash, salt):
    test_hash, _ = hash_password(password, salt)
    return test_hash == stored_hash

def get_live_event_stats(conn):
    c = conn.cursor()
    # 1. Registered teams and participants
    c.execute('SELECT COUNT(*) as cnt, COALESCE(SUM(team_size), 0) as participants FROM teams')
    row = c.fetchone()
    reg_teams = row['cnt'] if row else 0
    total_participants = row['participants'] if row else 0

    # 2. Participating teams
    c.execute("SELECT COUNT(DISTINCT team_id) as cnt FROM sessions WHERE session_status IN ('ACTIVE', 'COMPLETED')")
    row_part = c.fetchone()
    part_teams = row_part['cnt'] if row_part else 0
    if part_teams == 0 and reg_teams > 0:
        part_teams = reg_teams

    # 3. Completed investigations
    c.execute("SELECT COUNT(*) as cnt FROM submissions WHERE evaluation_status = 'EVALUATED'")
    row_comp = c.fetchone()
    completed = row_comp['cnt'] if row_comp else 0

    # 4. Disqualified teams
    c.execute("SELECT COUNT(*) as cnt FROM submissions WHERE qualification_status = 'DISQUALIFIED'")
    row_disq = c.fetchone()
    disqualified = row_disq['cnt'] if row_disq else 0

    # 5. Evaluations & Winners ranking
    c.execute('''
        SELECT sub.team_id, t.team_name, t.college_name, sub.total_score, sub.accuracy_rate, sub.qualification_status
        FROM submissions sub
        JOIN teams t ON sub.team_id = t.team_id
        ORDER BY sub.total_score DESC, sub.accuracy_rate DESC
    ''')
    results = []
    rows = c.fetchall()
    for idx, r in enumerate(rows):
        pos = ''
        recog = ''
        if idx == 0:
            pos = '1st Place — Winner'
            recog = 'Cyber Defense Champion (Forensic Excellence)'
        elif idx == 1:
            pos = '2nd Place — 1st Runner Up'
            recog = 'High Accuracy Investigator'
        elif idx == 2:
            pos = '3rd Place — 2nd Runner Up'
            recog = 'Commendable Speed & Analysis'
        else:
            pos = f'Rank {idx + 1}'
            recog = 'Certificate of Merit'

        results.append({
            'teamId': r['team_id'],
            'teamName': r['team_name'],
            'collegeName': r['college_name'] or 'T.J.S. Engineering College',
            'totalScore': r['total_score'],
            'accuracy': f"{r['accuracy_rate']:.1f}%",
            'finalStatus': r['qualification_status'],
            'winnerPosition': pos,
            'recognition': recog,
            'manualCorrectionReason': ''
        })

    return {
        'registeredTeams': reg_teams,
        'participatingTeams': part_teams,
        'totalParticipants': total_participants,
        'completedInvestigations': completed,
        'disqualifiedTeams': disqualified,
        'results': results
    }

def evaluate_team_submission(conn, team_id):
    """
    Authoritative backend grading engine. Evaluates participant answers
    against the authoritative question answer keys in SQLite.
    Computes score_r1, score_r2, total_score, accuracy_rate, and qualification_status.
    Preserves original automatically-calculated scores when manual corrections are applied.
    """
    c = conn.cursor()
    c.execute("SELECT * FROM submissions WHERE UPPER(team_id) = UPPER(?)", (team_id,))
    sub = c.fetchone()
    if not sub:
        return

    case_id = sub['case_id']
    if not case_id:
        return

    # Fetch authoritative answer keys for this case
    c.execute("SELECT id, round, order_num, correct_answer FROM questions WHERE case_id = ? ORDER BY round ASC, order_num ASC", (case_id,))
    q_rows = c.fetchall()
    if not q_rows:
        return None

    r1_keys = {r['order_num']: r['correct_answer'].strip().upper() for r in q_rows if r['round'] == 1}
    r2_keys = {r['order_num']: r['correct_answer'].strip().upper() for r in q_rows if r['round'] == 2}
    r1_ids = {r['order_num']: r['id'] for r in q_rows if r['round'] == 1}
    r2_ids = {r['order_num']: r['id'] for r in q_rows if r['round'] == 2}

    idx_to_letter = {
        0: 'A', 1: 'B', 2: 'C', 3: 'D',
        '0': 'A', '1': 'B', '2': 'C', '3': 'D',
        'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D',
        'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D'
    }

    # Parse manual corrections if any
    try:
        corrections = json.loads(sub['manual_corrections_json'] or '[]')
    except:
        corrections = []

    corr_map = {}
    for cr in corrections:
        try:
            corr_map[(int(cr.get('round', 1)), int(cr.get('orderNum', 1)))] = int(cr.get('newMark', 0))
        except:
            pass

    # Evaluate Round 1 (15 Questions)
    try:
        r1_ans = json.loads(sub['round1_answers_json'] or '{}')
    except:
        r1_ans = {}

    base_r1 = 0
    score_r1 = 0
    for q_num in range(1, 16):
        v = r1_ans.get(str(q_num - 1)) if str(q_num - 1) in r1_ans else r1_ans.get(q_num - 1)
        if v is None and str(q_num) in r1_ans:
            v = r1_ans.get(str(q_num))
        qid = r1_ids.get(q_num)
        if v is None and qid and qid in r1_ans:
            v = r1_ans.get(qid)

        user_letter = idx_to_letter.get(v, str(v).strip().upper() if v is not None else None)
        correct_letter = r1_keys.get(q_num)
        is_auto_correct = bool(correct_letter and user_letter == correct_letter)
        if is_auto_correct:
            base_r1 += 1

        if (1, q_num) in corr_map:
            score_r1 += corr_map[(1, q_num)]
        else:
            if is_auto_correct:
                score_r1 += 1

    # Evaluate Round 2 (15 Questions)
    try:
        r2_ans = json.loads(sub['round2_answers_json'] or '{}')
    except:
        r2_ans = {}

    base_r2 = 0
    score_r2 = 0
    for q_num in range(1, 16):
        v = r2_ans.get(str(q_num - 1)) if str(q_num - 1) in r2_ans else r2_ans.get(q_num - 1)
        if v is None and str(q_num) in r2_ans:
            v = r2_ans.get(str(q_num))
        qid = r2_ids.get(q_num)
        if v is None and qid and qid in r2_ans:
            v = r2_ans.get(qid)

        user_letter = idx_to_letter.get(v, str(v).strip().upper() if v is not None else None)
        correct_letter = r2_keys.get(q_num)
        is_auto_correct = bool(correct_letter and user_letter == correct_letter)
        if is_auto_correct:
            base_r2 += 1

        if (2, q_num) in corr_map:
            score_r2 += corr_map[(2, q_num)]
        else:
            if is_auto_correct:
                score_r2 += 1

    base_total = base_r1 + base_r2
    total_score = score_r1 + score_r2
    total_questions = len(r1_keys) + len(r2_keys) or 30
    accuracy_rate = round((total_score / float(total_questions)) * 100.0, 1)

    # Preserve original score if not set, or retain previous original
    existing_orig_r1 = sub['original_score_r1'] if 'original_score_r1' in sub.keys() else None
    existing_orig_r2 = sub['original_score_r2'] if 'original_score_r2' in sub.keys() else None
    existing_orig_tot = sub['original_total_score'] if 'original_total_score' in sub.keys() else None

    if existing_orig_tot is None:
        orig_r1 = base_r1
        orig_r2 = base_r2
        orig_tot = base_total
    else:
        orig_r1 = existing_orig_r1 if existing_orig_r1 is not None else base_r1
        orig_r2 = existing_orig_r2 if existing_orig_r2 is not None else base_r2
        orig_tot = existing_orig_tot

    # Check violations
    c.execute("SELECT COUNT(*) as vcnt FROM violations WHERE UPPER(team_id) = UPPER(?)", (team_id,))
    v_row = c.fetchone()
    vcnt = v_row['vcnt'] if v_row else (sub['violations_count'] or 0)

    prev_qual = sub['qualification_status']
    if vcnt >= 3:
        qual = 'DISQUALIFIED'
    elif prev_qual in ('QUALIFIED', 'NOT QUALIFIED', 'DISQUALIFIED'):
        qual = prev_qual
    else:
        # Default qualification threshold: score >= 20/30
        qual = 'QUALIFIED' if total_score >= 20 else 'NOT QUALIFIED'

    has_both = bool(sub['round1_answers_json'] and sub['round2_answers_json'])
    eval_status = 'EVALUATED' if has_both else (sub['evaluation_status'] or 'PENDING')

    c.execute('''
        UPDATE submissions SET
            score_r1 = ?, score_r2 = ?, total_score = ?, accuracy_rate = ?,
            original_score_r1 = ?, original_score_r2 = ?, original_total_score = ?,
            violations_count = ?, evaluation_status = ?, qualification_status = ?
        WHERE UPPER(team_id) = UPPER(?)
    ''', (score_r1, score_r2, total_score, accuracy_rate, orig_r1, orig_r2, orig_tot, vcnt, eval_status, qual, team_id))

    return {
        'scoreR1': score_r1,
        'scoreR2': score_r2,
        'totalScore': total_score,
        'accuracyRate': accuracy_rate,
        'originalTotalScore': orig_tot,
        'evaluationStatus': eval_status,
        'qualificationStatus': qual
    }


def get_team_progress(conn, team_id):
    """
    Computes and returns the authoritative logical state and progression telemetry
    for a specific team. Ensures complete isolation across teams.
    Logical States:
      - DEACTIVATED
      - TERMINATED
      - CASE_NOT_SELECTED
      - CASE_SELECTED
      - ROUND_1_IN_PROGRESS
      - ROUND_1_COMPLETED
      - ROUND_2_IN_PROGRESS
      - ROUND_2_COMPLETED
      - EVALUATION_PENDING
      - EVALUATION_COMPLETED
    """
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM teams WHERE UPPER(team_id) = UPPER(?)', (team_id,))
    team = c.fetchone()
    if not team:
        return None

    canonical_team_id = team['team_id']
    team_status = team['status']

    if team_status in ('Deactivated', 'DEACTIVATED'):
        return {
            'teamId': canonical_team_id,
            'teamName': team['team_name'],
            'status': team_status,
            'logicalState': 'DEACTIVATED',
            'isDeactivated': True
        }

    if team_status == 'Terminated':
        return {
            'teamId': canonical_team_id,
            'teamName': team['team_name'],
            'status': team_status,
            'logicalState': 'TERMINATED',
            'isTerminated': True
        }

    c.execute('SELECT * FROM sessions WHERE UPPER(team_id) = UPPER(?)', (canonical_team_id,))
    sess = c.fetchone()
    case_id = sess['case_id'] if sess else None
    case_name = sess['case_name'] if sess else None
    curr_round = sess['current_round'] if sess else 1
    sess_status = sess['session_status'] if sess else 'NOT STARTED'

    c.execute('SELECT * FROM submissions WHERE UPPER(team_id) = UPPER(?)', (canonical_team_id,))
    sub = c.fetchone()

    has_r1_answers = bool(sub and sub['round1_answers_json'] and sub['round1_answers_json'] != '{}')
    has_r2_answers = bool(sub and sub['round2_answers_json'] and sub['round2_answers_json'] != '{}')
    eval_status = sub['evaluation_status'] if sub else 'PENDING'

    now_ms = int(time.time() * 1000)

    # Check timers
    r1_timer_id = f"{canonical_team_id}_{case_id}_1" if case_id else None
    r2_timer_id = f"{canonical_team_id}_{case_id}_2" if case_id else None
    eval_timer_id = f"{canonical_team_id}_{case_id}_eval" if case_id else None

    r1_timer = None
    r2_timer = None
    eval_timer = None

    if r1_timer_id:
        c.execute('SELECT * FROM round_timers WHERE id = ?', (r1_timer_id,))
        r1_timer = c.fetchone()
    if r2_timer_id:
        c.execute('SELECT * FROM round_timers WHERE id = ?', (r2_timer_id,))
        r2_timer = c.fetchone()
    if eval_timer_id:
        c.execute('SELECT * FROM round_timers WHERE id = ?', (eval_timer_id,))
        eval_timer = c.fetchone()

    # R1 telemetry
    r1_started = bool(r1_timer)
    r1_submitted_early = bool(r1_timer and r1_timer['is_submitted_early'])
    r1_rem = max(0, int((r1_timer['end_time_ms'] - now_ms) / 1000)) if r1_timer else 600
    r1_completed = has_r1_answers or r1_submitted_early or (r1_timer and r1_rem <= 0) or (sess_status in ('ROUND 1 COMPLETED', 'SUBMITTED', 'COMPLETED'))

    # R2 telemetry
    r2_started = bool(r2_timer) or curr_round == 2 or (sess_status in ('ROUND_2_IN_PROGRESS', 'ROUND 2 IN PROGRESS'))
    r2_submitted_early = bool(r2_timer and r2_timer['is_submitted_early'])
    r2_rem = max(0, int((r2_timer['end_time_ms'] - now_ms) / 1000)) if r2_timer else 600
    r2_completed = has_r2_answers or r2_submitted_early or (r2_timer and r2_rem <= 0) or (sess_status in ('COMPLETED', 'EVALUATED'))

    # Evaluation telemetry
    eval_started = curr_round >= 3 or sess_status in ('EVALUATION', 'COMPLETED', 'EVALUATED') or (r1_completed and r2_completed)
    eval_completed = eval_status == 'EVALUATED' or (eval_timer and (now_ms >= eval_timer['end_time_ms']))

    # Determine explicit logical state
    if not case_id or case_id == 'PENDING SELECTION':
        logical_state = 'CASE_NOT_SELECTED'
    elif eval_completed:
        logical_state = 'EVALUATION_COMPLETED'
    elif eval_started or (r1_completed and r2_completed):
        logical_state = 'EVALUATION_PENDING'
    elif r2_started and not r2_completed:
        logical_state = 'ROUND_2_IN_PROGRESS'
    elif r1_completed and not r2_started:
        logical_state = 'ROUND_1_COMPLETED'
    elif r1_started and not r1_completed:
        logical_state = 'ROUND_1_IN_PROGRESS'
    else:
        logical_state = 'CASE_SELECTED'

    return {
        'teamId': canonical_team_id,
        'teamName': team['team_name'],
        'collegeName': team['college_name'],
        'department': team['department'],
        'status': team_status,
        'logicalState': logical_state,
        'caseId': case_id,
        'caseName': case_name,
        'currentRound': curr_round,
        'sessionStatus': sess_status,
        'hasParticipation': bool(case_id or r1_started or has_r1_answers or (sub and (sub['total_score'] or 0) > 0)),
        'round1': {
            'started': r1_started,
            'completed': r1_completed,
            'submittedEarly': r1_submitted_early,
            'remainingSeconds': r1_rem,
            'score': sub['score_r1'] if sub else 0
        },
        'round2': {
            'started': r2_started,
            'completed': r2_completed,
            'submittedEarly': r2_submitted_early,
            'remainingSeconds': r2_rem,
            'score': sub['score_r2'] if sub else 0
        },
        'evaluation': {
            'started': eval_started,
            'completed': eval_completed,
            'status': eval_status,
            'totalScore': sub['total_score'] if sub else 0,
            'qualificationStatus': sub['qualification_status'] if sub else 'RESULTS UNDER REVIEW'
        }
    }


def execute_complete_event_reset(conn, admin_id, phrase, backup_confirmed):
    """
    Executes an atomic, secure Complete Event Reset:
    1. Validates the confirmation phrase 'RESET TRACEX EVENT' and verified backup acknowledgment.
    2. Performs an automated online SQLite backup snapshot and verifies its file integrity and table records.
    3. Purges all previous participant data (teams, sessions, submissions, timers, violations, reports).
    4. Resets the global event state to 'EVENT NOT STARTED' and phase to 'STANDBY'.
    5. Preserves administrator credentials, the 15 investigation cases, the question bank, and audit logs.
    """
    if phrase != 'RESET TRACEX EVENT':
        return 400, {
            'error': "Confirmation phrase mismatch. You must enter exact confirmation phrase 'RESET TRACEX EVENT' to proceed."
        }

    if not backup_confirmed:
        return 400, {
            'error': "You must review the affected data categories and confirm that a verified database backup exists."
        }

    # 1. Automatic Pre-Reset Database Backup & Integrity Verification
    now_iso = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    timestamp_str = time.strftime('%Y%m%d_%H%M%S', time.gmtime())
    backup_id = f"BKP-RESET-{secrets.token_hex(4).upper()}"
    filename = f"tracex_backup_pre_reset_{timestamp_str}.db"
    file_path = os.path.join(BACKUP_DIR, filename)

    try:
        os.makedirs(BACKUP_DIR, exist_ok=True)
        # Perform consistent snapshot using SQLite Online Backup API directly from active connection
        dest_conn = sqlite3.connect(file_path)
        conn.backup(dest_conn)
        dest_conn.close()

        # Verify backup file existence and size
        if not os.path.exists(file_path):
            raise Exception("Backup file not found after creation.")
        file_size = os.path.getsize(file_path)
        if file_size <= 0:
            raise Exception("Backup file is empty (0 bytes).")

        # Verify backup database integrity and critical tables
        verify_conn = sqlite3.connect(file_path)
        vc = verify_conn.cursor()
        vc.execute("SELECT COUNT(*) FROM cases")
        cases_count = vc.fetchone()[0]
        vc.execute("SELECT COUNT(*) FROM questions")
        questions_count = vc.fetchone()[0]
        vc.execute("SELECT COUNT(*) FROM admins")
        admins_count = vc.fetchone()[0]
        verify_conn.close()

        if cases_count != 15 or questions_count < 15 or admins_count < 1:
            raise Exception(f"Backup verification failed: incomplete records (cases={cases_count}, questions={questions_count}, admins={admins_count}).")

        # Register backup record in backups table
        c = conn.cursor()
        c.execute('''
            INSERT INTO backups (backup_id, filename, file_path, file_size, created_by, created_at, status, details)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (backup_id, filename, file_path, file_size, admin_id, now_iso, 'COMPLETED', f"Verified pre-reset snapshot created prior to complete event wipe by {admin_id}"))

    except Exception as bkp_err:
        return 500, {
            'error': f"CRITICAL: Complete event reset aborted. Could not create verified database backup: {str(bkp_err)}"
        }

    # 2. Database Atomic Purge within Transaction
    try:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")

        # Count previous records for audit trail
        c.execute("SELECT COUNT(*) FROM teams")
        teams_cleared = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM submissions")
        subs_cleared = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM sessions")
        sess_cleared = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM violations")
        viol_cleared = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM round_timers")
        timers_cleared = c.fetchone()[0]

        # Purge participant & event data tables in foreign-key safe order
        c.execute("DELETE FROM team_sessions")
        c.execute("DELETE FROM round_timers")
        c.execute("DELETE FROM score_audit_logs")
        c.execute("DELETE FROM violations")
        c.execute("DELETE FROM submissions")
        c.execute("DELETE FROM sessions")
        c.execute("DELETE FROM teams")
        c.execute("DELETE FROM event_report_versions")
        c.execute("DELETE FROM event_reports")
        try:
            c.execute("DELETE FROM sqlite_sequence WHERE name IN ('violations', 'score_audit_logs', 'event_reports', 'event_report_versions', 'teams')")
        except:
            pass

        # Reset Event State to EVENT NOT STARTED & STANDBY
        c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('status', 'EVENT NOT STARTED')")
        c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('phase', 'STANDBY')")
        c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('round', '1')")
        c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('round1_start_time', '')")
        c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('round1_end_time', '')")
        c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('round2_start_time', '')")
        c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('round2_end_time', '')")
        c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('eval_start_time', '')")
        c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('eval_end_time', '')")
        c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('results_published', '0')")
        c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('results_finalized', '0')")
        c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('official_winner_team_id', '')")
        c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('official_winner_reason', '')")
        c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('official_winner_admin_id', '')")
        c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('official_winner_at', '')")
        c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('published_by', '')")
        c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('published_at', '')")
        c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('finalized_by', '')")
        c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('finalized_at', '')")

        # Reset resultsPublished in settings JSON while preserving general settings
        c.execute("SELECT value FROM event_state WHERE key = 'settings'")
        sett_row = c.fetchone()
        settings = json.loads(sett_row[0]) if sett_row else {}
        settings['resultsPublished'] = False
        c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('settings', ?)", (json.dumps(settings),))

        # Flag that initial demo seeding has already occurred so restart does not re-seed demo teams
        c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('initial_teams_seeded', '1')")

        # 3. Record Complete Reset in Audit Logs
        c.execute('''
            INSERT INTO audit_logs (admin_id, action, details, prev_value, new_value, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (admin_id, 'COMPLETE_EVENT_RESET',
              f"COMPLETE EVENT RESET executed by {admin_id}. Verified backup: {filename} ({file_size} bytes). Cleared: {teams_cleared} teams, {subs_cleared} submissions, {sess_cleared} sessions, {viol_cleared} violations, {timers_cleared} timers. State set to EVENT NOT STARTED / STANDBY.",
              'PREVIOUS_EVENT_DATA', 'EVENT NOT STARTED', now_iso))

        conn.commit()

        return 200, {
            'success': True,
            'message': 'Complete event reset executed successfully. Previous event data cleared, verified backup stored, and system restored to STANDBY.',
            'status': 'EVENT NOT STARTED',
            'eventStatus': 'EVENT NOT STARTED',
            'phase': 'STANDBY',
            'databaseTarget': DB_FILE,
            'environment': os.environ.get('VERCEL_ENV', os.environ.get('ENV', 'local')),
            'backup': {
                'backupId': backup_id,
                'filename': filename,
                'fileSize': file_size,
                'createdAt': now_iso
            },
            'cleared': {
                'teams': teams_cleared,
                'submissions': subs_cleared,
                'sessions': sess_cleared,
                'violations': viol_cleared,
                'timers': timers_cleared
            },
            'preserved': {
                'cases': 15,
                'questions': 450,
                'adminPreserved': True
            }
        }
    except Exception as reset_err:
        conn.rollback()
        return 500, {
            'error': f"Transaction failed during complete event reset: {str(reset_err)}"
        }


def init_database():
    conn = get_db()
    c = conn.cursor()

    # 1. Admins Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            admin_id TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')

    # 2. Admin Sessions Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS admin_sessions (
            token TEXT PRIMARY KEY,
            admin_id TEXT NOT NULL,
            created_at REAL NOT NULL,
            expires_at REAL NOT NULL
        )
    ''')

    # 3. Teams Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            team_id TEXT PRIMARY KEY,
            team_name TEXT NOT NULL,
            college_name TEXT NOT NULL,
            department TEXT NOT NULL,
            team_size INTEGER NOT NULL,
            members_json TEXT NOT NULL,
            pin_masked TEXT NOT NULL,
            pin_hash TEXT NOT NULL,
            pin_salt TEXT NOT NULL,
            registered_at TEXT NOT NULL,
            status TEXT NOT NULL,
            registration_number INTEGER UNIQUE
        )
    ''')
    c.execute("PRAGMA table_info(teams)")
    existing_team_cols = {row['name'] for row in c.fetchall()}
    if 'registration_number' not in existing_team_cols:
        c.execute("ALTER TABLE teams ADD COLUMN registration_number INTEGER")
    c.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_teams_reg_num ON teams(registration_number)")

    # 4. Live Participant Sessions
    c.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            team_id TEXT PRIMARY KEY,
            case_id TEXT,
            case_name TEXT,
            current_round INTEGER DEFAULT 1,
            current_question INTEGER DEFAULT 1,
            time_remaining TEXT DEFAULT '10:00',
            connection_status TEXT DEFAULT 'SECURE',
            session_status TEXT DEFAULT 'NOT STARTED',
            updated_at REAL NOT NULL
        )
    ''')

    # 5. Security Violations Log
    c.execute('''
        CREATE TABLE IF NOT EXISTS violations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_id TEXT NOT NULL,
            violation_type TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            violation_count INTEGER NOT NULL,
            action_taken TEXT NOT NULL
        )
    ''')

    # 6. Evaluation Submissions & Results
    c.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            team_id TEXT PRIMARY KEY,
            case_id TEXT NOT NULL,
            round1_answers_json TEXT,
            round2_answers_json TEXT,
            score_r1 INTEGER DEFAULT 0,
            score_r2 INTEGER DEFAULT 0,
            total_score INTEGER DEFAULT 0,
            accuracy_rate REAL DEFAULT 0,
            violations_count INTEGER DEFAULT 0,
            evaluation_status TEXT DEFAULT 'PENDING',
            qualification_status TEXT DEFAULT 'RESULTS UNDER REVIEW',
            submitted_at TEXT NOT NULL
        )
    ''')

    # 7. Event State & Configuration
    c.execute('''
        CREATE TABLE IF NOT EXISTS event_state (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    ''')

    # 8. Administrator Audit Log
    c.execute('''
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_id TEXT NOT NULL,
            action TEXT NOT NULL,
            details TEXT NOT NULL,
            prev_value TEXT,
            new_value TEXT,
            timestamp TEXT NOT NULL
        )
    ''')

    # 9. Final Event Reports Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS event_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            status TEXT DEFAULT 'DRAFT',
            version INTEGER DEFAULT 1,
            title TEXT NOT NULL,
            college_name TEXT NOT NULL,
            department_name TEXT NOT NULL,
            event_date TEXT NOT NULL,
            event_venue TEXT NOT NULL,
            organizer TEXT NOT NULL,
            coordinators TEXT NOT NULL,
            overview_json TEXT NOT NULL,
            participation_json TEXT NOT NULL,
            structure_json TEXT NOT NULL,
            results_json TEXT NOT NULL,
            summary_json TEXT NOT NULL,
            organizers_json TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            updated_by TEXT NOT NULL,
            published_at TEXT,
            published_by TEXT
        )
    ''')

    # 10. Event Report Version History Snapshots
    c.execute('''
        CREATE TABLE IF NOT EXISTS event_report_versions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_id INTEGER NOT NULL,
            version INTEGER NOT NULL,
            status TEXT NOT NULL,
            data_json TEXT NOT NULL,
            saved_by TEXT NOT NULL,
            saved_at TEXT NOT NULL,
            change_summary TEXT
        )
    ''')

    # 11. Investigation Cases Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS cases (
            case_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            summary TEXT NOT NULL,
            evidence_json TEXT NOT NULL,
            round2_evidence_json TEXT NOT NULL,
            status TEXT DEFAULT 'ACTIVE',
            order_idx INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            updated_by TEXT NOT NULL
        )
    ''')

    # 12. Authoritative Questionnaire & Answer Keys Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id TEXT PRIMARY KEY,
            case_id TEXT NOT NULL,
            round INTEGER NOT NULL,
            order_num INTEGER NOT NULL,
            question_text TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            marks INTEGER DEFAULT 1,
            evidence_ref TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            updated_by TEXT NOT NULL,
            FOREIGN KEY (case_id) REFERENCES cases(case_id)
        )
    ''')

    # 13. Database Backups Registry Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS backups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            backup_id TEXT NOT NULL,
            filename TEXT NOT NULL,
            file_path TEXT NOT NULL,
            file_size INTEGER NOT NULL,
            created_by TEXT NOT NULL,
            created_at TEXT NOT NULL,
            status TEXT DEFAULT 'COMPLETED',
            details TEXT
        )
    ''')

    # 14. Administrative Export Logs Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS export_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            export_type TEXT NOT NULL,
            format TEXT NOT NULL,
            admin_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            status TEXT NOT NULL,
            record_count INTEGER
        )
    ''')

    # 15. Authoritative Investigation Round Timers
    c.execute('''
        CREATE TABLE IF NOT EXISTS round_timers (
            id TEXT PRIMARY KEY,
            team_id TEXT NOT NULL,
            case_id TEXT NOT NULL,
            round INTEGER NOT NULL,
            start_time_ms INTEGER NOT NULL,
            end_time_ms INTEGER NOT NULL,
            duration_sec INTEGER NOT NULL,
            is_submitted_early INTEGER DEFAULT 0,
            submitted_at_ms INTEGER DEFAULT 0
        )
    ''')

    # Seed Default Administrator if not present
    c.execute('SELECT admin_id FROM admins WHERE admin_id = ?', ('admin_cse',))
    if not c.fetchone():
        admin_default_pwd = os.environ.get('TRACEX_ADMIN_PASSWORD', 'traceX@2026')
        h, s = hash_password(admin_default_pwd)
        c.execute('''
            INSERT INTO admins (admin_id, password_hash, salt, name, role, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('admin_cse', h, s, 'CSE Technical Faculty', 'SUPERADMIN', time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())))

    # Seed Initial Event State if not present
    default_state = {
        'status': 'EVENT NOT STARTED',
        'phase': 'REGISTRATION & STANDBY',
        'round': '1',
        'settings': json.dumps({
            'eventAvailable': True,
            'registrationAvailable': True,
            'round1Duration': 10,
            'round2Duration': 10,
            'evalDuration': 5,
            'violationThreshold': 3,
            'resultsPublished': False
        })
    }
    for k, v in default_state.items():
        c.execute('INSERT OR IGNORE INTO event_state (key, value) VALUES (?, ?)', (k, v))

    # Seed Initial Registered Teams if empty and never previously seeded/reset
    c.execute("SELECT value FROM event_state WHERE key = 'initial_teams_seeded'")
    seeded_row = c.fetchone()
    c.execute('SELECT COUNT(*) as cnt FROM teams')
    row = c.fetchone()
    if (not seeded_row or seeded_row['value'] != '1') and row and row['cnt'] == 0:
        demo_teams = [
            {
                'team_id': 'TX-2026-9042',
                'team_name': 'CyberDefenders',
                'college_name': 'TJS Engineering College',
                'department': 'Computer Science & Engineering',
                'team_size': 2,
                'members': ['Aravind K', 'Siddharth M'],
                'pin': '7491',
                'status': 'Investigating',
                'case_id': 'case-01',
                'case_name': 'CASE 01 — STOLEN SOCIAL MEDIA ACCOUNT',
                'round': 2,
                'q': 8,
                'time': '04:15',
                'conn': 'SECURE',
                'sess_status': 'ACTIVE',
                'r1_score': 13,
                'r2_score': 12,
                'total': 25,
                'acc': 83.3,
                'qual': 'RESULTS UNDER REVIEW'
            },
            {
                'team_id': 'TX-2026-8815',
                'team_name': 'ZeroDay Hunters',
                'college_name': 'R.M.K. Engineering College',
                'department': 'Information Technology',
                'team_size': 3,
                'members': ['Karthik R', 'Deepak N', 'Vijay S'],
                'pin': '8204',
                'status': 'Submitted',
                'case_id': 'case-02',
                'case_name': 'CASE 02 — UNSECURED WI-FI SNIFFING',
                'round': 2,
                'q': 15,
                'time': '00:00',
                'conn': 'SECURE',
                'sess_status': 'SUBMITTED',
                'r1_score': 14,
                'r2_score': 13,
                'total': 27,
                'acc': 90.0,
                'qual': 'RESULTS UNDER REVIEW'
            },
            {
                'team_id': 'TX-2026-7640',
                'team_name': 'Kernel Enforcers',
                'college_name': 'St. Joseph College of Engineering',
                'department': 'Computer Science',
                'team_size': 1,
                'members': ['Manoj Kumar V'],
                'pin': '3912',
                'status': 'Registered',
                'case_id': None,
                'case_name': 'PENDING SELECTION',
                'round': 1,
                'q': 1,
                'time': '10:00',
                'conn': 'STANDBY',
                'sess_status': 'NOT STARTED',
                'r1_score': 0,
                'r2_score': 0,
                'total': 0,
                'acc': 0,
                'qual': 'RESULTS UNDER REVIEW'
            },
            {
                'team_id': 'TX-2026-6194',
                'team_name': 'BitShield Ops',
                'college_name': 'TJS Engineering College',
                'department': 'Cyber Security',
                'team_size': 4,
                'members': ['Pooja S', 'Nivetha R', 'Swathi G', 'Rithika B'],
                'pin': '6149',
                'status': 'Terminated',
                'case_id': 'case-04',
                'case_name': 'CASE 04 — MALICIOUS USB DROP AT WORKPLACE',
                'round': 1,
                'q': 5,
                'time': '06:12',
                'conn': 'DISCONNECTED',
                'sess_status': 'TERMINATED',
                'r1_score': 3,
                'r2_score': 0,
                'total': 3,
                'acc': 20.0,
                'qual': 'DISQUALIFIED'
            }
        ]

        now_iso = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        for tm in demo_teams:
            ph, ps = hash_password(tm['pin'])
            c.execute('''
                INSERT INTO teams (team_id, team_name, college_name, department, team_size, members_json, pin_masked, pin_hash, pin_salt, registered_at, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                tm['team_id'], tm['team_name'], tm['college_name'], tm['department'],
                tm['team_size'], json.dumps(tm['members']), '••••••', ph, ps, now_iso, tm['status']
            ))

            c.execute('''
                INSERT INTO sessions (team_id, case_id, case_name, current_round, current_question, time_remaining, connection_status, session_status, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                tm['team_id'], tm['case_id'], tm['case_name'], tm['round'], tm['q'],
                tm['time'], tm['conn'], tm['sess_status'], time.time()
            ))

            c.execute('''
                INSERT INTO submissions (team_id, case_id, score_r1, score_r2, total_score, accuracy_rate, violations_count, evaluation_status, qualification_status, submitted_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                tm['team_id'], tm['case_id'] or 'case-01', tm['r1_score'], tm['r2_score'],
                tm['total'], tm['acc'], 1 if tm['status'] == 'Terminated' else 0,
                'EVALUATED' if tm['status'] in ('Submitted', 'Terminated') else 'PENDING',
                tm['qual'], now_iso
            ))

        # Seed initial violation records
        c.execute('''
            INSERT INTO violations (team_id, violation_type, timestamp, violation_count, action_taken)
            VALUES (?, ?, ?, ?, ?)
        ''', ('TX-2026-6194', 'TAB SWITCH', now_iso, 1, 'Warning 1 of 3: Incident recorded'))
        c.execute('''
            INSERT INTO violations (team_id, violation_type, timestamp, violation_count, action_taken)
            VALUES (?, ?, ?, ?, ?)
        ''', ('TX-2026-6194', 'WINDOW LEAVE', now_iso, 2, 'Critical Warning 2 of 3'))
        c.execute('''
            INSERT INTO violations (team_id, violation_type, timestamp, violation_count, action_taken)
            VALUES (?, ?, ?, ?, ?)
        ''', ('TX-2026-6194', 'FULLSCREEN EXIT', now_iso, 3, 'Terminated: Exceeded Max Allowed Violations'))
        c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('initial_teams_seeded', '1')")
    # -------------------------------------------------------------------------
    # Idempotent Schema Migrations & Participant Session Table
    # -------------------------------------------------------------------------
    c.execute("PRAGMA table_info(submissions)")
    existing_sub_cols = {row['name'] for row in c.fetchall()}
    if 'original_score_r1' not in existing_sub_cols:
        c.execute("ALTER TABLE submissions ADD COLUMN original_score_r1 INTEGER")
    if 'original_score_r2' not in existing_sub_cols:
        c.execute("ALTER TABLE submissions ADD COLUMN original_score_r2 INTEGER")
    if 'original_total_score' not in existing_sub_cols:
        c.execute("ALTER TABLE submissions ADD COLUMN original_total_score INTEGER")
    if 'manual_corrections_json' not in existing_sub_cols:
        c.execute("ALTER TABLE submissions ADD COLUMN manual_corrections_json TEXT DEFAULT '[]'")
    if 'winner_declaration' not in existing_sub_cols:
        c.execute("ALTER TABLE submissions ADD COLUMN winner_declaration TEXT DEFAULT 'SYSTEM_CALCULATED'")
    if 'override_reason' not in existing_sub_cols:
        c.execute("ALTER TABLE submissions ADD COLUMN override_reason TEXT DEFAULT ''")
    if 'score_last_modified_at' not in existing_sub_cols:
        c.execute("ALTER TABLE submissions ADD COLUMN score_last_modified_at TEXT")
    if 'score_modified_by' not in existing_sub_cols:
        c.execute("ALTER TABLE submissions ADD COLUMN score_modified_by TEXT")
    if 'is_score_adjusted' not in existing_sub_cols:
        c.execute("ALTER TABLE submissions ADD COLUMN is_score_adjusted INTEGER DEFAULT 0")

    # Authoritative Team Registration Number Sequence
    c.execute("PRAGMA table_info(teams)")
    existing_team_cols = {row['name'] for row in c.fetchall()}
    if 'registration_number' not in existing_team_cols:
        c.execute("ALTER TABLE teams ADD COLUMN registration_number INTEGER")
    c.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_teams_reg_num ON teams(registration_number)")

    # SURREAL: Final Score Management Audit Trail Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS score_audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_id TEXT NOT NULL,
            original_score INTEGER NOT NULL,
            prev_final_score INTEGER NOT NULL,
            new_final_score INTEGER NOT NULL,
            admin_id TEXT NOT NULL,
            reason TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')

    # Team Sessions Table for Participant Authentication
    c.execute('''
        CREATE TABLE IF NOT EXISTS team_sessions (
            token TEXT PRIMARY KEY,
            team_id TEXT NOT NULL,
            created_at REAL NOT NULL,
            expires_at REAL NOT NULL
        )
    ''')

    # Seed Default Event State keys for Finalization & Publication
    default_state_keys = {
        'results_finalized': '0',
        'finalized_by': '',
        'finalized_at': '',
        'results_published': '0',
        'published_by': '',
        'published_at': '',
        'official_winner_team_id': '',
        'official_winner_reason': '',
        'official_winner_admin_id': '',
        'official_winner_at': ''
    }
    for k, v in default_state_keys.items():
        c.execute('INSERT OR IGNORE INTO event_state (key, value) VALUES (?, ?)', (k, v))

    # Ensure demo teams have realistic submitted answers for testing and demonstration
    demo_teams_seed_answers = [
        ('TX-2026-8815', 'case-02', 14, 13),
        ('TX-2026-9042', 'case-01', 13, 12),
        ('TX-2026-7640', 'case-03', 11, 10),
        ('TX-2026-6194', 'case-04', 3, 0),
        ('TX-2026-TEAM', 'case-01', 12, 11)
    ]
    for tm_id, cid, target_r1, target_r2 in demo_teams_seed_answers:
        c.execute("SELECT round1_answers_json, round2_answers_json FROM submissions WHERE UPPER(team_id) = UPPER(?)", (tm_id,))
        s_row = c.fetchone()
        if s_row:
            has_r1 = bool(s_row['round1_answers_json'] and s_row['round1_answers_json'] != '{}')
            has_r2 = bool(s_row['round2_answers_json'] and s_row['round2_answers_json'] != '{}')
            if not has_r1 or not has_r2:
                # Fetch question keys for this case
                c.execute("SELECT round, order_num, correct_answer FROM questions WHERE case_id = ? ORDER BY round, order_num", (cid,))
                q_list = c.fetchall()
                if q_list:
                    r1_q = [q for q in q_list if q['round'] == 1]
                    r2_q = [q for q in q_list if q['round'] == 2]
                    alt_map = {'A': 'B', 'B': 'C', 'C': 'D', 'D': 'A'}

                    r1_dict = {}
                    for idx_q, q in enumerate(r1_q):
                        cor = q['correct_answer'].strip().upper()
                        ans = cor if idx_q < target_r1 else alt_map.get(cor, 'A')
                        r1_dict[str(idx_q)] = ans

                    r2_dict = {}
                    for idx_q, q in enumerate(r2_q):
                        cor = q['correct_answer'].strip().upper()
                        ans = cor if idx_q < target_r2 else alt_map.get(cor, 'A')
                        r2_dict[str(idx_q)] = ans

                    c.execute('''
                        UPDATE submissions SET
                            case_id = ?,
                            round1_answers_json = ?,
                            round2_answers_json = ?,
                            evaluation_status = 'EVALUATED'
                        WHERE UPPER(team_id) = UPPER(?)
                    ''', (cid, json.dumps(r1_dict), json.dumps(r2_dict), tm_id))
                    evaluate_team_submission(conn, tm_id)

    # Seed 15 Investigation Cases and 450 Questions if table empty
    seed_cases_and_questions(conn)

    conn.commit()
    conn.close()


def seed_cases_and_questions(conn):
    c = conn.cursor()
    c.execute("SELECT COUNT(*) as cnt FROM cases")
    row = c.fetchone()
    if row and row['cnt'] > 0:
        return

    seed_file = os.path.join(os.path.dirname(__file__), 'cases_seed.json')
    if not os.path.exists(seed_file):
        print("[TRACE × X] cases_seed.json not found, skipping case seeding.")
        return

    try:
        with open(seed_file, 'r', encoding='utf-8') as f:
            cases_data = json.load(f)
    except Exception as e:
        print(f"[TRACE × X] Error reading cases_seed.json: {e}")
        return

    now_iso = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    for idx, (cid, case) in enumerate(cases_data.items()):
        name = case.get('name', f'CASE {idx+1}')
        summary = case.get('summary', '')
        evidence = case.get('evidence', [])
        round2_evidence = case.get('round2Evidence', [])

        c.execute('''
            INSERT OR REPLACE INTO cases (case_id, name, summary, evidence_json, round2_evidence_json, status, order_idx, created_at, updated_at, updated_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            cid, name, summary, json.dumps(evidence), json.dumps(round2_evidence),
            'ACTIVE', idx + 1, now_iso, now_iso, 'SYSTEM_INITIAL_SEED'
        ))

        # Seed Round 1 questions
        for q_idx, q in enumerate(case.get('questions', [])):
            qid = f"{cid}-r1-q{q_idx+1:02d}"
            opts = q.get('options', ['', '', '', ''])
            ans_idx = q.get('answer', 0)
            ans_letter = ['A', 'B', 'C', 'D'][ans_idx] if 0 <= ans_idx < 4 else 'A'
            c.execute('''
                INSERT OR REPLACE INTO questions (id, case_id, round, order_num, question_text, option_a, option_b, option_c, option_d, correct_answer, marks, evidence_ref, created_at, updated_at, updated_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                qid, cid, 1, q_idx + 1, q.get('text', ''),
                opts[0] if len(opts) > 0 else '',
                opts[1] if len(opts) > 1 else '',
                opts[2] if len(opts) > 2 else '',
                opts[3] if len(opts) > 3 else '',
                ans_letter, 1, evidence[q_idx % len(evidence)]['title'] if evidence else '',
                now_iso, now_iso, 'SYSTEM_INITIAL_SEED'
            ))

        # Seed Round 2 questions
        for q_idx, q in enumerate(case.get('round2Questions', [])):
            qid = f"{cid}-r2-q{q_idx+1:02d}"
            opts = q.get('options', ['', '', '', ''])
            ans_idx = q.get('answer', 0)
            ans_letter = ['A', 'B', 'C', 'D'][ans_idx] if 0 <= ans_idx < 4 else 'A'
            c.execute('''
                INSERT OR REPLACE INTO questions (id, case_id, round, order_num, question_text, option_a, option_b, option_c, option_d, correct_answer, marks, evidence_ref, created_at, updated_at, updated_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                qid, cid, 2, q_idx + 1, q.get('text', ''),
                opts[0] if len(opts) > 0 else '',
                opts[1] if len(opts) > 1 else '',
                opts[2] if len(opts) > 2 else '',
                opts[3] if len(opts) > 3 else '',
                ans_letter, 1, round2_evidence[q_idx % len(round2_evidence)]['title'] if round2_evidence else '',
                now_iso, now_iso, 'SYSTEM_INITIAL_SEED'
            ))

    print(f"[TRACE × X] Successfully seeded {len(cases_data)} cases and 450 authoritative questions into SQLite.")

# -----------------------------------------------------------------------------
# HTTP Request Handler
# -----------------------------------------------------------------------------
class TraceXRequestHandler(SimpleHTTPRequestHandler):

    def send_json(self, status_code, data):
        payload = json.dumps(data).encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(payload)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.end_headers()
        self.wfile.write(payload)

    def send_csv(self, filename, fieldnames, rows):
        output = io.StringIO()
        output.write('\ufeff') # UTF-8 BOM for Microsoft Excel compatibility
        writer = csv.DictWriter(output, fieldnames=fieldnames, lineterminator='\r\n')
        writer.writeheader()
        for r in rows:
            safe_r = {}
            for k, v in r.items():
                if isinstance(v, str) and v and (v[0] in ('=', '+', '@') or (v[0] == '-' and len(v) > 1 and not v[1:].replace('.', '', 1).isdigit())):
                    # Guard against CSV / Spreadsheet formula injection (CWE-1236)
                    safe_r[k] = "'" + v
                else:
                    safe_r[k] = v
            writer.writerow(safe_r)
        payload = output.getvalue().encode('utf-8')

        self.send_response(200)
        self.send_header('Content-Type', 'text/csv; charset=utf-8')
        self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
        self.send_header('Content-Length', str(len(payload)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.end_headers()
        self.wfile.write(payload)

    def send_binary(self, filename, content_type, data):
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.end_headers()
        self.wfile.write(data)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
        self.end_headers()

    def resolve_api_path(self):
        url = urlparse(self.path)
        path = url.path.rstrip('/')
        if not path:
            path = '/'
        query = parse_qs(url.query)

        # 1. Direct /api/ route
        if path.startswith('/api/') and not path.startswith('/api/index'):
            return path, query

        # 2. Check query parameter passed from Vercel rewrite (__path=...)
        if '__path' in query and query['__path']:
            sub = query['__path'][0].lstrip('/').rstrip('/')
            return f'/api/{sub}', query

        # 3. Check Vercel / proxy routing headers
        for hdr in ('x-vercel-matched-path', 'x-matched-path', 'x-now-route-matches', 'x-forwarded-uri', 'x-original-uri', 'x-envoy-original-path'):
            hdr_val = self.headers.get(hdr)
            if hdr_val:
                hdr_path = urlparse(hdr_val).path.rstrip('/')
                if hdr_path.startswith('/api/') and not hdr_path.startswith('/api/index'):
                    return hdr_path, query

        return path, query

    def get_token_admin(self):
        auth_header = self.headers.get('Authorization', '')
        token = ''
        if auth_header.startswith('Bearer '):
            token = auth_header[7:].strip()
        else:
            cookie = self.headers.get('Cookie', '')
            for part in cookie.split(';'):
                if 'traceX_admin_token=' in part:
                    token = part.split('traceX_admin_token=')[1].strip()

        if not token:
            return None

        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT * FROM admin_sessions WHERE token = ? AND expires_at > ?', (token, time.time()))
        row = c.fetchone()
        conn.close()
        if row:
            return row['admin_id']
        return None

    def get_token_team(self):
        auth_header = self.headers.get('Authorization', '')
        token = ''
        if auth_header.startswith('Bearer '):
            token = auth_header[7:].strip()
        else:
            cookie = self.headers.get('Cookie', '')
            for part in cookie.split(';'):
                if 'traceX_team_token=' in part:
                    token = part.split('traceX_team_token=')[1].strip()

        if not token:
            query = parse_qs(urlparse(self.path).query)
            token = query.get('token', [''])[0].strip()

        if not token:
            return None

        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT * FROM team_sessions WHERE token = ? AND expires_at > ?', (token, time.time()))
        row = c.fetchone()
        conn.close()
        if row:
            return row['team_id']
        return None

    def read_json_body(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            if length > 0:
                raw = self.rfile.read(length).decode('utf-8')
                return json.loads(raw) if raw else {}
        except Exception:
            pass
        return {}

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    # -------------------------------------------------------------------------
    # GET Handlers
    # -------------------------------------------------------------------------
    def do_GET(self):
        path, query = self.resolve_api_path()

        if not path.startswith('/api/'):
            return super().do_GET()

        conn = get_db()
        c = conn.cursor()

        # 1. System Health Check
        if path == '/api/health':
            conn.close()
            return self.send_json(200, {'status': 'healthy', 'system': 'TRACE × X Engine', 'version': '2.0.0'})

        # 2. Public Event Status
        if path == '/api/event/status':
            c.execute('SELECT key, value FROM event_state')
            rows = c.fetchall()
            st = {r['key']: r['value'] for r in rows}
            c.execute('SELECT COUNT(*) as cnt FROM teams')
            reg_count = c.fetchone()['cnt']
            conn.close()
            return self.send_json(200, {
                'status': st.get('status', 'EVENT NOT STARTED'),
                'phase': st.get('phase', 'STANDBY'),
                'round': st.get('round', '1'),
                'registeredTeams': reg_count,
                'registrationCount': reg_count
            })

        # 2a2. Public Registration Count
        if path == '/api/teams/count':
            c.execute('SELECT COUNT(*) as count, COALESCE(MAX(registration_number), 0) + 1 as next_num FROM teams')
            row = c.fetchone()
            cnt = row['count']
            next_num = row['next_num']
            conn.close()
            return self.send_json(200, {
                'count': cnt,
                'registeredTeams': cnt,
                'nextRegistrationNumber': next_num
            })

        # 2b. Public Participant-Facing Cases List (STRICT PRIVACY: ONLY Case Name & Short Description)
        if path == '/api/cases':
            c.execute("SELECT case_id as id, name, summary, status FROM cases WHERE status = 'ACTIVE' ORDER BY order_idx ASC")
            cases = [dict(r) for r in c.fetchall()]
            conn.close()
            return self.send_json(200, {'cases': cases})

        # 2c. Public Participant Questions (STRICT PRIVACY: Answer key and marks omitted)
        if path == '/api/cases/questions':
            cid = query.get('case_id', [''])[0]
            rnd = int(query.get('round', ['1'])[0])
            team_id = query.get('team_id', [''])[0].strip()

            if team_id:
                c.execute('SELECT case_id, status FROM teams t LEFT JOIN sessions s ON UPPER(t.team_id) = UPPER(s.team_id) WHERE UPPER(t.team_id) = UPPER(?)', (team_id,))
                s_row = c.fetchone()
                if s_row:
                    if s_row['status'] in ('Deactivated', 'DEACTIVATED'):
                        conn.close()
                        return self.send_json(403, {'error': 'Team account is deactivated. Access denied.'})
                    if s_row['status'] == 'Terminated':
                        conn.close()
                        return self.send_json(403, {'error': 'Team account is terminated. Access denied.'})
                    if s_row['case_id'] and s_row['case_id'] != cid:
                        conn.close()
                        return self.send_json(403, {'error': f"Case access denied. Your assigned case is {s_row['case_id']}."})

            c.execute('''
                SELECT id, case_id, round, order_num, question_text, option_a, option_b, option_c, option_d, evidence_ref
                FROM questions
                WHERE case_id = ? AND round = ?
                ORDER BY order_num ASC
            ''', (cid, rnd))
            qs = []
            for r in c.fetchall():
                qs.append({
                    'id': r['id'],
                    'caseId': r['case_id'],
                    'round': r['round'],
                    'orderNum': r['order_num'],
                    'text': r['question_text'],
                    'options': [r['option_a'], r['option_b'], r['option_c'], r['option_d']],
                    'evidenceRef': r['evidence_ref']
                })
            conn.close()
            return self.send_json(200, {'questions': qs})

        # 2c2. Team-Specific Progress & Authoritative State
        if path == '/api/teams/progress':
            team_id = query.get('team_id', [''])[0].strip()
            if not team_id:
                token_team = self.get_token_team()
                if token_team:
                    team_id = token_team

            if not team_id:
                conn.close()
                return self.send_json(400, {'error': 'Team ID is required.'})

            prog = get_team_progress(conn, team_id)
            if not prog:
                conn.close()
                return self.send_json(404, {'error': f"Team '{team_id}' not found."})

            if prog.get('isDeactivated'):
                conn.close()
                return self.send_json(403, {'error': 'This team account has been deactivated.', 'isDeactivated': True})
            if prog.get('isTerminated'):
                conn.close()
                return self.send_json(403, {'error': 'This team account has been terminated.', 'isTerminated': True})

            conn.close()
            return self.send_json(200, {'success': True, 'progress': prog})

        # 2d. Authoritative Investigation Round Timer (Independent Per-Team Timers)
        if path == '/api/round/timer':
            team_id = query.get('team_id', ['TX-2026-TEAM'])[0].strip()
            case_id = query.get('case_id', ['case-01'])[0].strip()
            rnd_param = str(query.get('round', ['1'])[0]).lower().strip()
            if rnd_param in ('eval', '3', 'evaluation'):
                rnd = 'eval'
            else:
                try:
                    rnd = int(rnd_param)
                except (ValueError, TypeError):
                    rnd = 1

            now_ms = int(time.time() * 1000)

            # Check team status
            c.execute('SELECT status FROM teams WHERE UPPER(team_id) = UPPER(?)', (team_id,))
            t_row = c.fetchone()
            if not t_row:
                conn.close()
                return self.send_json(404, {'error': f"Team '{team_id}' not found."})
            if t_row['status'] in ('Deactivated', 'DEACTIVATED'):
                conn.close()
                return self.send_json(403, {'error': 'Team account is deactivated. Access denied.'})
            if t_row['status'] == 'Terminated':
                conn.close()
                return self.send_json(403, {'error': 'Team account is terminated. Access denied.'})

            c.execute("SELECT key, value FROM event_state WHERE key IN ('status', 'phase', 'round', 'settings')")
            ev_rows = {r['key']: r['value'] for r in c.fetchall()}
            ev_status = ev_rows.get('status', 'EVENT ACTIVE')

            # Parse configurable durations from settings
            try:
                sett = json.loads(ev_rows.get('settings', '{}'))
            except:
                sett = {}

            if rnd == 'eval':
                dur_sec = int(sett.get('evalDuration', 5)) * 60
            elif rnd == 2:
                dur_sec = int(sett.get('round2Duration', 10)) * 60
            else:
                dur_sec = int(sett.get('round1Duration', 10)) * 60

            if dur_sec <= 0:
                dur_sec = 300 if rnd == 'eval' else 600

            timer_id = f"{team_id}_{case_id}_{rnd}"
            c.execute('SELECT * FROM round_timers WHERE id = ?', (timer_id,))
            timer_row = c.fetchone()

            if timer_row:
                st_ms = timer_row['start_time_ms']
                end_ms = timer_row['end_time_ms']
                dur_sec = timer_row['duration_sec'] or dur_sec
                rem_sec = max(0, min(dur_sec, int((end_ms - now_ms) / 1000)))
                is_sub = timer_row['is_submitted_early']
            else:
                # Fresh, independent round timer for THIS specific team
                st_ms = now_ms
                end_ms = now_ms + (dur_sec * 1000)
                rem_sec = dur_sec
                is_sub = 0
                c.execute('''
                    INSERT INTO round_timers (id, team_id, case_id, round, start_time_ms, end_time_ms, duration_sec, is_submitted_early, submitted_at_ms)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 0, 0)
                ''', (timer_id, team_id, case_id, 3 if rnd == 'eval' else rnd, st_ms, end_ms, dur_sec))

            mins = rem_sec // 60
            secs = rem_sec % 60
            active_round_num = 3 if rnd == 'eval' else rnd
            
            c.execute('''
                UPDATE sessions
                SET case_id = COALESCE(case_id, ?),
                    current_round = ?, 
                    time_remaining = ?, 
                    session_status = CASE 
                        WHEN session_status IN ('SUBMITTED', 'ROUND 1 COMPLETED', 'COMPLETED', 'DEACTIVATED', 'TERMINATED') THEN session_status 
                        ELSE ? 
                    END, 
                    updated_at = ?
                WHERE UPPER(team_id) = UPPER(?)
            ''', (case_id, active_round_num, f"{mins:02d}:{secs:02d}", 'EVALUATION' if rnd == 'eval' else f'ROUND_{rnd}_IN_PROGRESS', time.time(), team_id))
            conn.commit()

            conn.close()
            return self.send_json(200, {
                'serverTime': now_ms,
                'eventStatus': ev_status,
                'isStarted': True,
                'phase': ev_rows.get('phase', 'ACTIVE'),
                'round': rnd,
                'startTime': st_ms,
                'endTime': end_ms,
                'duration': dur_sec,
                'durationSeconds': dur_sec,
                'remainingSeconds': rem_sec,
                'isExpired': rem_sec <= 0,
                'isSubmittedEarly': bool(is_sub)
            })

        # 2e. Public Participant Result Status (Strict Privacy Guard)
        if path == '/api/participant/result':
            team_id = query.get('team_id', [''])[0].strip()
            c.execute("SELECT key, value FROM event_state WHERE key IN ('settings', 'results_published')")
            st_map = {r['key']: r['value'] for r in c.fetchall()}
            sett = json.loads(st_map.get('settings', '{}'))
            if 'resultsPublished' in sett:
                is_published = bool(sett['resultsPublished'])
            else:
                is_published = st_map.get('results_published') == '1'

            if not is_published:
                conn.close()
                return self.send_json(200, {
                    'status': 'RESULTS UNDER REVIEW',
                    'isPublished': False,
                    'heading': 'INVESTIGATION COMPLETE',
                    'subheading': 'RESULTS UNDER REVIEW',
                    'message': 'Your investigation has been submitted successfully. Final results will be available after the organizers publish them.'
                })

            token_team_id = self.get_token_team()
            target_id = token_team_id if token_team_id else team_id

            c.execute("SELECT qualification_status FROM submissions WHERE UPPER(team_id) = UPPER(?)", (target_id,))
            sub = c.fetchone()
            qual = sub['qualification_status'] if sub else 'RESULTS UNDER REVIEW'
            conn.close()
            return self.send_json(200, {
                'status': qual,
                'isPublished': True,
                'teamId': target_id
            })

        # ------------------- PROTECTED ADMIN API -----------------------------
        admin_id = self.get_token_admin()
        if not admin_id:
            conn.close()
            return self.send_json(401, {'error': 'Unauthorized: Admin authentication required.'})

        # 3. Admin Overview Dashboard
        if path == '/api/admin/overview':
            c.execute('SELECT COUNT(*) as count FROM teams')
            reg_count = c.fetchone()['count']

            c.execute("SELECT COUNT(*) as count FROM sessions WHERE session_status = 'ACTIVE'")
            active_count = c.fetchone()['count']

            c.execute("SELECT COUNT(*) as count FROM submissions WHERE evaluation_status = 'EVALUATED'")
            completed_count = c.fetchone()['count']

            c.execute('SELECT COUNT(*) as count FROM violations')
            violation_count = c.fetchone()['count']

            c.execute('SELECT key, value FROM event_state')
            st = {r['key']: r['value'] for r in c.fetchall()}

            conn.close()
            return self.send_json(200, {
                'registeredTeams': reg_count,
                'activeParticipants': active_count,
                'completedInvestigations': completed_count,
                'activeViolations': violation_count,
                'eventStatus': st.get('status', 'EVENT NOT STARTED'),
                'currentPhase': st.get('phase', 'STANDBY'),
                'isLiveDatabase': True
            })

        # 4. Team Management List
        if path == '/api/admin/teams':
            c.execute('''
                SELECT t.team_id, t.team_name, t.college_name, t.department, t.team_size, t.members_json, t.registered_at, t.status, t.registration_number,
                       s.case_id, s.case_name, s.current_round, s.session_status,
                       sub.total_score, sub.evaluation_status, sub.round1_answers_json, sub.round2_answers_json
                FROM teams t
                LEFT JOIN sessions s ON UPPER(t.team_id) = UPPER(s.team_id)
                LEFT JOIN submissions sub ON UPPER(t.team_id) = UPPER(sub.team_id)
                ORDER BY t.registered_at DESC
            ''')
            teams = []
            for r in c.fetchall():
                has_part = bool(
                    (r['case_id'] and r['session_status'] not in ('NOT STARTED', 'PENDING SELECTION')) or 
                    (r['round1_answers_json'] and r['round1_answers_json'] != '{}') or 
                    (r['round2_answers_json'] and r['round2_answers_json'] != '{}') or 
                    ((r['total_score'] or 0) > 0)
                )
                teams.append({
                    'teamId': r['team_id'],
                    'teamName': r['team_name'],
                    'collegeName': r['college_name'],
                    'department': r['department'],
                    'teamSize': r['team_size'],
                    'members': json.loads(r['members_json']),
                    'registeredAt': r['registered_at'],
                    'status': r['status'],
                    'registrationNumber': r['registration_number'],
                    'selectedCaseId': r['case_id'] or None,
                    'selectedCaseName': r['case_name'] or 'Pending Selection',
                    'currentRound': r['current_round'] or 1,
                    'sessionStatus': r['session_status'] or 'NOT STARTED',
                    'score': r['total_score'] if (r['total_score'] is not None and r['evaluation_status'] == 'EVALUATED') else None,
                    'hasParticipation': has_part
                })
            conn.close()
            return self.send_json(200, {'teams': teams})

        # 5. Live Sessions List
        if path == '/api/admin/sessions':
            c.execute('''
                SELECT s.team_id, t.team_name, s.case_id, s.case_name, s.current_round, s.current_question, 
                       s.time_remaining, s.connection_status, s.session_status, s.updated_at
                FROM sessions s
                JOIN teams t ON s.team_id = t.team_id
                ORDER BY s.updated_at DESC
            ''')
            sessions = []
            for r in c.fetchall():
                sessions.append({
                    'teamId': r['team_id'],
                    'teamName': r['team_name'],
                    'caseId': r['case_id'] or 'UNSELECTED',
                    'caseName': r['case_name'] or 'CASE PENDING',
                    'currentRound': r['current_round'],
                    'currentQuestion': r['current_question'],
                    'timeRemaining': r['time_remaining'],
                    'connectionStatus': r['connection_status'],
                    'sessionStatus': r['session_status']
                })
            conn.close()
            return self.send_json(200, {'sessions': sessions})

        # 6. Round Control Status
        if path == '/api/admin/round-control':
            c.execute('SELECT key, value FROM event_state')
            st = {r['key']: r['value'] for r in c.fetchall()}

            c.execute("SELECT COUNT(*) as cnt FROM sessions WHERE session_status = 'SUBMITTED'")
            submitted_count = c.fetchone()['cnt']

            c.execute('SELECT COUNT(*) as cnt FROM teams')
            total_teams = c.fetchone()['cnt']

            conn.close()
            return self.send_json(200, {
                'currentRound': int(st.get('round', 1)),
                'eventStatus': st.get('status', 'EVENT NOT STARTED'),
                'currentPhase': st.get('phase', 'STANDBY'),
                'round1Duration': 10,
                'round1Questions': 15,
                'round2Duration': 10,
                'round2Questions': 15,
                'evalDuration': 5,
                'submittedCount': submitted_count,
                'totalTeams': total_teams
            })

        # 7. Violations Log List
        if path == '/api/admin/violations':
            c.execute('''
                SELECT v.id, v.team_id, t.team_name, v.violation_type, v.timestamp, v.violation_count, v.action_taken
                FROM violations v
                LEFT JOIN teams t ON v.team_id = t.team_id
                ORDER BY v.id DESC
            ''')
            logs = []
            for r in c.fetchall():
                logs.append({
                    'id': r['id'],
                    'teamId': r['team_id'],
                    'teamName': r['team_name'] or 'UNKNOWN TEAM',
                    'type': r['violation_type'],
                    'timestamp': r['timestamp'],
                    'count': r['violation_count'],
                    'action': r['action_taken']
                })
            conn.close()
            return self.send_json(200, {'violations': logs})

        # 8. Evaluation & Results Matrix
        if path == '/api/admin/evaluations':
            c.execute("SELECT key, value FROM event_state WHERE key IN ('results_finalized', 'results_published', 'official_winner_team_id', 'settings')")
            ev_state = {r['key']: r['value'] for r in c.fetchall()}
            sett = json.loads(ev_state.get('settings', '{}'))
            is_finalized = ev_state.get('results_finalized') == '1'
            if 'resultsPublished' in sett:
                is_published = bool(sett['resultsPublished'])
            else:
                is_published = ev_state.get('results_published') == '1'
            official_winner_id = ev_state.get('official_winner_team_id', '')

            c.execute('''
                SELECT sub.team_id, t.team_name, sub.case_id, c.name as case_name,
                       sub.score_r1, sub.score_r2, sub.total_score, sub.original_total_score,
                       sub.accuracy_rate, sub.violations_count, sub.evaluation_status, sub.qualification_status, 
                       sub.manual_corrections_json, sub.winner_declaration, sub.override_reason,
                       sub.submitted_at
                FROM submissions sub
                JOIN teams t ON sub.team_id = t.team_id
                LEFT JOIN cases c ON sub.case_id = c.case_id
                ORDER BY sub.total_score DESC, sub.accuracy_rate DESC, sub.violations_count ASC
            ''')
            evals = []
            rows = c.fetchall()
            for idx, r in enumerate(rows):
                try:
                    corr_list = json.loads(r['manual_corrections_json'] or '[]')
                except:
                    corr_list = []
                has_corr = len(corr_list) > 0

                is_sys_winner = (idx == 0)
                is_decl_winner = (official_winner_id.upper() == r['team_id'].upper()) if official_winner_id else is_sys_winner

                evals.append({
                    'teamId': r['team_id'],
                    'teamName': r['team_name'],
                    'caseId': r['case_id'],
                    'caseName': r['case_name'] or r['case_id'],
                    'r1Status': 'COMPLETED (15/15)',
                    'r2Status': 'COMPLETED (15/15)' if r['score_r2'] > 0 or r['evaluation_status'] == 'EVALUATED' else 'IN PROGRESS',
                    'scoreR1': r['score_r1'],
                    'scoreR2': r['score_r2'],
                    'totalScore': r['total_score'],
                    'originalTotalScore': r['original_total_score'] if r['original_total_score'] is not None else r['total_score'],
                    'hasCorrections': has_corr,
                    'accuracy': f"{r['accuracy_rate']:.1f}%",
                    'violations': r['violations_count'],
                    'evaluationStatus': r['evaluation_status'],
                    'finalStatus': r['qualification_status'],
                    'winnerDeclaration': r['winner_declaration'] or 'SYSTEM_CALCULATED',
                    'overrideReason': r['override_reason'] or '',
                    'isSystemWinner': is_sys_winner,
                    'isDeclaredWinner': is_decl_winner,
                    'isFinalized': is_finalized,
                    'isPublished': is_published,
                    'submittedAt': r['submitted_at']
                })
            conn.close()
            return self.send_json(200, {
                'evaluations': evals,
                'resultsFinalized': is_finalized,
                'resultsPublished': is_published,
                'officialWinnerTeamId': official_winner_id
            })

        # 8b. Detailed Answer Review (All 30 questions: Round 1 & Round 2)
        if path == '/api/admin/submissions/detail':
            team_id = query.get('teamId', query.get('team_id', ['']))[0].strip()
            if not team_id:
                conn.close()
                return self.send_json(400, {'error': 'teamId parameter is required.'})

            c.execute('''
                SELECT sub.*, t.team_name, t.college_name, t.department, c.name as case_name
                FROM submissions sub
                JOIN teams t ON sub.team_id = t.team_id
                LEFT JOIN cases c ON sub.case_id = c.case_id
                WHERE UPPER(sub.team_id) = UPPER(?)
            ''', (team_id,))
            sub_row = c.fetchone()
            if not sub_row:
                conn.close()
                return self.send_json(404, {'error': f"Submission record for team {team_id} not found."})

            case_id = sub_row['case_id']
            # Fetch all questions for this case
            c.execute('SELECT * FROM questions WHERE case_id = ? ORDER BY round ASC, order_num ASC', (case_id,))
            q_rows = c.fetchall()

            # Parse participant answers
            try: r1_answers = json.loads(sub_row['round1_answers_json'] or '{}')
            except: r1_answers = {}
            try: r2_answers = json.loads(sub_row['round2_answers_json'] or '{}')
            except: r2_answers = {}
            try: corrections = json.loads(sub_row['manual_corrections_json'] or '[]')
            except: corrections = []

            corr_map = {}
            for cr in corrections:
                try: corr_map[(int(cr.get('round', 1)), int(cr.get('orderNum', 1)))] = cr
                except: pass

            idx_to_letter = {0: 'A', 1: 'B', 2: 'C', 3: 'D', '0': 'A', '1': 'B', '2': 'C', '3': 'D',
                             'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D'}
            letter_to_idx = {'A': 0, 'B': 1, 'C': 2, 'D': 3}

            def build_round_detail(round_num, ans_dict):
                round_qs = [q for q in q_rows if q['round'] == round_num]
                items = []
                submitted_cnt = 0
                correct_cnt = 0
                incorrect_cnt = 0
                unanswered_cnt = 0
                round_score = 0

                for q in round_qs:
                    order = q['order_num']
                    options = [q['option_a'], q['option_b'], q['option_c'], q['option_d']]
                    corr_letter = q['correct_answer'].strip().upper()
                    corr_idx = letter_to_idx.get(corr_letter, 0)
                    corr_text = options[corr_idx] if 0 <= corr_idx < 4 else ''

                    raw_val = None
                    if str(order - 1) in ans_dict:
                        raw_val = ans_dict[str(order - 1)]
                    elif order - 1 in ans_dict:
                        raw_val = ans_dict[order - 1]
                    elif str(order) in ans_dict:
                        raw_val = ans_dict[str(order)]
                    elif q['id'] in ans_dict:
                        raw_val = ans_dict[q['id']]

                    is_answered = raw_val is not None and str(raw_val).strip() != ''
                    user_letter = idx_to_letter.get(raw_val, str(raw_val).strip().upper()) if is_answered else None
                    user_idx = letter_to_idx.get(user_letter) if user_letter else None
                    user_text = options[user_idx] if (user_idx is not None and 0 <= user_idx < 4) else (str(user_letter) if user_letter else 'UNANSWERED')

                    # Structure options as dictionary with A, B, C, D
                    options_dict = {
                        'A': options[0] if len(options) > 0 else '',
                        'B': options[1] if len(options) > 1 else '',
                        'C': options[2] if len(options) > 2 else '',
                        'D': options[3] if len(options) > 3 else ''
                    }

                    auto_correct = bool(is_answered and user_letter == corr_letter)
                    base_mark = 1 if auto_correct else 0

                    if is_answered:
                        submitted_cnt += 1
                        if auto_correct:
                            status_str = 'CORRECT'
                            correct_cnt += 1
                        else:
                            status_str = 'INCORRECT'
                            incorrect_cnt += 1
                    else:
                        unanswered_cnt += 1
                        status_str = 'UNANSWERED'

                    # Check manual correction
                    corr_info = corr_map.get((round_num, order))
                    if corr_info:
                        mark_awarded = int(corr_info.get('newMark', base_mark))
                        is_corrected = True
                        corr_reason = corr_info.get('reason', '')
                        corr_admin = corr_info.get('adminId', '')
                        corr_time = corr_info.get('timestamp', '')
                    else:
                        mark_awarded = base_mark
                        is_corrected = False
                        corr_reason = ''
                        corr_admin = ''
                        corr_time = ''

                    round_score += mark_awarded

                    items.append({
                        'id': q['id'],
                        'questionId': q['id'],
                        'caseId': q['case_id'],
                        'round': round_num,
                        'orderNum': order,
                        'questionText': q['question_text'],
                        'options': options_dict,
                        'submittedAnswer': user_letter,
                        'submittedOptionText': user_text,
                        'correctAnswer': corr_letter,
                        'correctOptionText': corr_text,
                        'isAnswered': is_answered,
                        'isCorrect': auto_correct,
                        'status': status_str,
                        'marksAwarded': mark_awarded,
                        'maxMarks': 1,
                        'isManuallyCorrected': is_corrected,
                        'correctionReason': corr_reason,
                        'correctionAdmin': corr_admin,
                        'correctionTimestamp': corr_time,
                        'evidenceRef': q['evidence_ref'] or ''
                    })

                summary = {
                    'totalQuestions': len(round_qs),
                    'submittedAnswers': submitted_cnt,
                    'correctAnswers': correct_cnt,
                    'incorrectAnswers': incorrect_cnt,
                    'unansweredQuestions': unanswered_cnt,
                    'roundResult': round_score,
                    'maxMarks': len(round_qs)
                }
                return items, summary

            r1_items, r1_summary = build_round_detail(1, r1_answers)
            r2_items, r2_summary = build_round_detail(2, r2_answers)

            total_q = r1_summary['totalQuestions'] + r2_summary['totalQuestions']
            total_sub = r1_summary['submittedAnswers'] + r2_summary['submittedAnswers']
            total_corr = r1_summary['correctAnswers'] + r2_summary['correctAnswers']
            total_inc = r1_summary['incorrectAnswers'] + r2_summary['incorrectAnswers']
            total_un = r1_summary['unansweredQuestions'] + r2_summary['unansweredQuestions']
            total_sc = r1_summary['roundResult'] + r2_summary['roundResult']
            acc_rate = round((total_sc / float(total_q or 30)) * 100.0, 1)

            c.execute("SELECT key, value FROM event_state WHERE key IN ('results_finalized', 'results_published')")
            ev_map = {r['key']: r['value'] for r in c.fetchall()}

            conn.close()
            team_meta = {
                'teamId': sub_row['team_id'],
                'teamName': sub_row['team_name'],
                'collegeName': sub_row['college_name'],
                'department': sub_row['department'],
                'caseId': sub_row['case_id'],
                'caseName': sub_row['case_name'] or sub_row['case_id'],
                'evaluationStatus': sub_row['evaluation_status'],
                'qualificationStatus': sub_row['qualification_status'],
                'violationsCount': sub_row['violations_count'],
                'submittedAt': sub_row['submitted_at'],
                'winnerDeclaration': sub_row['winner_declaration'] or 'SYSTEM_CALCULATED',
                'overrideReason': sub_row['override_reason'] or ''
            }

            overall_meta = {
                'totalQuestions': total_q,
                'submittedAnswers': total_sub,
                'correctAnswers': total_corr,
                'incorrectAnswers': total_inc,
                'unansweredQuestions': total_un,
                'totalScore': total_sc,
                'maxMarks': total_q,
                'accuracy': f"{acc_rate:.1f}%",
                'originalScoreR1': sub_row['original_score_r1'],
                'originalScoreR2': sub_row['original_score_r2'],
                'originalTotalScore': sub_row['original_total_score'] if sub_row['original_total_score'] is not None else sub_row['total_score'],
                'hasManualCorrections': len(corrections) > 0,
                'corrections': corrections,
                'isFinalized': ev_map.get('results_finalized') == '1',
                'isPublished': ev_map.get('results_published') == '1'
            }

            conn.close()
            return self.send_json(200, {
                'success': True,
                'team': team_meta,
                'round1': {
                    'questions': r1_items,
                    'summary': r1_summary
                },
                'round2': {
                    'questions': r2_items,
                    'summary': r2_summary
                },
                'overall': overall_meta,
                'submission': {
                    'teamId': sub_row['team_id'],
                    'teamName': sub_row['team_name'],
                    'caseId': sub_row['case_id'],
                    'caseName': sub_row['case_name'] or sub_row['case_id'],
                    'scoreR1': r1_summary['roundResult'],
                    'scoreR2': r2_summary['roundResult'],
                    'totalScore': total_sc,
                    'originalScoreR1': sub_row['original_score_r1'],
                    'originalScoreR2': sub_row['original_score_r2'],
                    'originalTotalScore': sub_row['original_total_score'] if sub_row['original_total_score'] is not None else sub_row['total_score'],
                    'hasCorrections': len(corrections) > 0,
                    'winnerDeclaration': sub_row['winner_declaration'] or 'SYSTEM_CALCULATED',
                    'overrideReason': sub_row['override_reason'] or '',
                    'round1': r1_items,
                    'round2': r2_items,
                    'round1Summary': r1_summary,
                    'round2Summary': r2_summary,
                    'overall': overall_meta
                }
            })

        # 8d. Final Winner Review & Decision Matrix
        if path == '/api/admin/winner-review':
            c.execute('''
                SELECT sub.team_id, t.team_name, t.college_name, sub.case_id, c.name as case_name,
                       sub.score_r1, sub.score_r2, sub.total_score, sub.accuracy_rate,
                       sub.violations_count, sub.evaluation_status, sub.qualification_status,
                       sub.winner_declaration, sub.override_reason, sub.manual_corrections_json
                FROM submissions sub
                JOIN teams t ON sub.team_id = t.team_id
                LEFT JOIN cases c ON sub.case_id = c.case_id
                ORDER BY sub.total_score DESC, sub.accuracy_rate DESC, sub.violations_count ASC
            ''')
            rows = c.fetchall()

            c.execute("SELECT key, value FROM event_state WHERE key IN ('results_finalized', 'results_published', 'finalized_by', 'finalized_at', 'published_by', 'published_at', 'official_winner_team_id', 'official_winner_reason', 'official_winner_admin_id', 'official_winner_at', 'settings')")
            ev_state = {r['key']: r['value'] for r in c.fetchall()}
            sett = json.loads(ev_state.get('settings', '{}'))

            is_finalized = ev_state.get('results_finalized') == '1'
            if 'resultsPublished' in sett:
                is_published = bool(sett['resultsPublished'])
            else:
                is_published = ev_state.get('results_published') == '1'
            official_winner_id = (ev_state.get('official_winner_team_id') or '').strip()

            ranked_teams = []
            sys_winner = None
            decl_winner = None

            for idx, r in enumerate(rows):
                rank = idx + 1
                try:
                    corr_list = json.loads(r['manual_corrections_json'] or '[]')
                except:
                    corr_list = []

                t_obj = {
                    'teamId': r['team_id'],
                    'teamName': r['team_name'],
                    'collegeName': r['college_name'],
                    'caseId': r['case_id'],
                    'caseName': r['case_name'] or r['case_id'],
                    'scoreR1': r['score_r1'],
                    'scoreR2': r['score_r2'],
                    'totalScore': r['total_score'],
                    'accuracy': f"{r['accuracy_rate']:.1f}%",
                    'systemRank': rank,
                    'violationsCount': r['violations_count'],
                    'violationStatus': 'DISQUALIFIED' if r['violations_count'] >= 3 else (f"{r['violations_count']} VIOLATIONS" if r['violations_count'] > 0 else '0 (CLEAN)'),
                    'evaluationStatus': r['evaluation_status'],
                    'finalStatus': r['qualification_status'],
                    'hasCorrections': len(corr_list) > 0,
                    'winnerDeclaration': r['winner_declaration'] or 'SYSTEM_CALCULATED',
                    'overrideReason': r['override_reason'] or ''
                }

                if idx == 0:
                    sys_winner = dict(t_obj)
                    sys_winner['type'] = 'SYSTEM_CALCULATED'

                if official_winner_id and r['team_id'].upper() == official_winner_id.upper():
                    decl_winner = dict(t_obj)
                    decl_winner['type'] = 'OFFICIALLY_DECLARED_OVERRIDE'
                    decl_winner['reason'] = ev_state.get('official_winner_reason', '')
                    decl_winner['adminId'] = ev_state.get('official_winner_admin_id', '')
                    decl_winner['timestamp'] = ev_state.get('official_winner_at', '')

                ranked_teams.append(t_obj)

            if not decl_winner:
                decl_winner = dict(sys_winner) if sys_winner else None
                if decl_winner:
                    decl_winner['type'] = 'SYSTEM_CALCULATED'

            is_overridden = bool(sys_winner and decl_winner and sys_winner['teamId'] != decl_winner['teamId'])

            conn.close()
            return self.send_json(200, {
                'systemCalculatedWinner': sys_winner,
                'officialDeclaredWinner': decl_winner,
                'isOverridden': is_overridden,
                'overrideReason': ev_state.get('official_winner_reason', ''),
                'overrideAdmin': ev_state.get('official_winner_admin_id', ''),
                'overrideTimestamp': ev_state.get('official_winner_at', ''),
                'resultsFinalized': is_finalized,
                'resultsPublished': is_published,
                'finalizedBy': ev_state.get('finalized_by', ''),
                'finalizedAt': ev_state.get('finalized_at', ''),
                'publishedBy': ev_state.get('published_by', ''),
                'publishedAt': ev_state.get('published_at', ''),
                'teams': ranked_teams
            })

        # 9. Event Settings
        if path == '/api/admin/settings':
            c.execute("SELECT value FROM event_state WHERE key = 'settings'")
            row = c.fetchone()
            settings = json.loads(row['value']) if row else {}
            conn.close()
            return self.send_json(200, {'settings': settings})

        # 10. Audit Logs List
        if path == '/api/admin/audit-logs':
            c.execute('SELECT id, admin_id, action, details, prev_value, new_value, timestamp FROM audit_logs ORDER BY id DESC LIMIT 50')
            logs = []
            for r in c.fetchall():
                logs.append({
                    'id': r['id'],
                    'adminId': r['admin_id'],
                    'action': r['action'],
                    'details': r['details'],
                    'prevValue': r['prev_value'],
                    'newValue': r['new_value'],
                    'timestamp': r['timestamp']
                })
            conn.close()
            return self.send_json(200, {'auditLogs': logs})

        # 11. Final Report Active Record
        if path == '/api/admin/report':
            c.execute('SELECT * FROM event_reports ORDER BY id DESC LIMIT 1')
            row = c.fetchone()
            live_stats = get_live_event_stats(conn)
            if not row:
                conn.close()
                return self.send_json(200, {
                    'hasReport': False,
                    'report': None,
                    'liveStats': live_stats
                })

            report = {
                'id': row['id'],
                'status': row['status'],
                'version': row['version'],
                'title': row['title'],
                'collegeName': row['college_name'],
                'departmentName': row['department_name'],
                'eventDate': row['event_date'],
                'eventVenue': row['event_venue'],
                'organizer': row['organizer'],
                'coordinators': row['coordinators'],
                'overview': json.loads(row['overview_json']),
                'participation': json.loads(row['participation_json']),
                'structure': json.loads(row['structure_json']),
                'results': json.loads(row['results_json']),
                'summary': json.loads(row['summary_json']),
                'organizers': json.loads(row['organizers_json']),
                'createdAt': row['created_at'],
                'updatedAt': row['updated_at'],
                'updatedBy': row['updated_by'],
                'publishedAt': row['published_at'],
                'publishedBy': row['published_by']
            }
            conn.close()
            return self.send_json(200, {
                'hasReport': True,
                'report': report,
                'liveStats': live_stats
            })

        # 12. Final Report Live Stats
        if path == '/api/admin/report/live-stats':
            live_stats = get_live_event_stats(conn)
            conn.close()
            return self.send_json(200, {'liveStats': live_stats})

        # 13. Final Report Versions History
        if path == '/api/admin/report/versions':
            c.execute('SELECT id, report_id, version, status, saved_by, saved_at, change_summary FROM event_report_versions ORDER BY id DESC LIMIT 50')
            versions = []
            for r in c.fetchall():
                versions.append({
                    'id': r['id'],
                    'reportId': r['report_id'],
                    'version': r['version'],
                    'status': r['status'],
                    'savedBy': r['saved_by'],
                    'savedAt': r['saved_at'],
                    'changeSummary': r['change_summary']
                })
            conn.close()
            return self.send_json(200, {'versions': versions})

        # 14. Admin Cases List with Question Counts
        if path == '/api/admin/cases':
            c.execute('''
                SELECT c.*,
                       (SELECT COUNT(*) FROM questions q WHERE q.case_id = c.case_id AND q.round = 1) as r1_count,
                       (SELECT COUNT(*) FROM questions q WHERE q.case_id = c.case_id AND q.round = 2) as r2_count
                FROM cases c
                ORDER BY c.order_idx ASC
            ''')
            cases = []
            for r in c.fetchall():
                try: ev = json.loads(r['evidence_json'])
                except: ev = []
                try: r2ev = json.loads(r['round2_evidence_json'])
                except: r2ev = []
                cases.append({
                    'caseId': r['case_id'],
                    'name': r['name'],
                    'summary': r['summary'],
                    'status': r['status'],
                    'orderIdx': r['order_idx'],
                    'r1Count': r['r1_count'],
                    'r2Count': r['r2_count'],
                    'totalQuestions': r['r1_count'] + r['r2_count'],
                    'evidenceCount': len(ev),
                    'round2EvidenceCount': len(r2ev),
                    'updatedAt': r['updated_at'],
                    'updatedBy': r['updated_by']
                })
            conn.close()
            return self.send_json(200, {'cases': cases})

        # 15. Admin Case Detail & Complete Questionnaire
        if path == '/api/admin/cases/detail':
            cid = query.get('id', ['case-01'])[0]
            c.execute('SELECT * FROM cases WHERE case_id = ?', (cid,))
            crow = c.fetchone()
            if not crow:
                conn.close()
                return self.send_json(404, {'error': f"Case {cid} not found."})

            c.execute('SELECT * FROM questions WHERE case_id = ? ORDER BY round ASC, order_num ASC', (cid,))
            r1_questions = []
            r2_questions = []
            for q in c.fetchall():
                q_obj = {
                    'id': q['id'],
                    'caseId': q['case_id'],
                    'round': q['round'],
                    'orderNum': q['order_num'],
                    'text': q['question_text'],
                    'optionA': q['option_a'],
                    'optionB': q['option_b'],
                    'optionC': q['option_c'],
                    'optionD': q['option_d'],
                    'options': [q['option_a'], q['option_b'], q['option_c'], q['option_d']],
                    'correctAnswer': q['correct_answer'],
                    'marks': q['marks'],
                    'evidenceRef': q['evidence_ref'] or '',
                    'updatedAt': q['updated_at']
                }
                if q['round'] == 1:
                    r1_questions.append(q_obj)
                else:
                    r2_questions.append(q_obj)

            try: ev = json.loads(crow['evidence_json'])
            except: ev = []
            try: r2ev = json.loads(crow['round2_evidence_json'])
            except: r2ev = []

            # Check event state lock status
            c.execute("SELECT value FROM event_state WHERE key = 'status'")
            st_row = c.fetchone()
            ev_status = st_row['value'] if st_row else 'EVENT NOT STARTED'
            is_locked = ev_status in ('EVENT ACTIVE', 'EVENT PAUSED')

            conn.close()
            return self.send_json(200, {
                'case': {
                    'caseId': crow['case_id'],
                    'name': crow['name'],
                    'summary': crow['summary'],
                    'evidence': ev,
                    'round2Evidence': r2ev,
                    'status': crow['status'],
                    'orderIdx': crow['order_idx'],
                    'updatedAt': crow['updated_at'],
                    'updatedBy': crow['updated_by']
                },
                'round1Questions': r1_questions,
                'round2Questions': r2_questions,
                'eventStatus': ev_status,
                'isLocked': is_locked
            })

        # 16. Comprehensive Case & Question Bank Readiness Validation
        if path == '/api/admin/cases/validation':
            c.execute('''
                SELECT c.case_id, c.name, c.status,
                       (SELECT COUNT(*) FROM questions q WHERE q.case_id = c.case_id AND q.round = 1) as r1_cnt,
                       (SELECT COUNT(*) FROM questions q WHERE q.case_id = c.case_id AND q.round = 2) as r2_cnt
                FROM cases c
                ORDER BY c.order_idx ASC
            ''')
            all_cases = c.fetchall()
            validation_list = []
            issues = []
            for cs in all_cases:
                cid = cs['case_id']
                r1 = cs['r1_cnt']
                r2 = cs['r2_cnt']
                c_issues = []
                if r1 != 15:
                    c_issues.append(f"Round 1 has {r1} questions (Required: exactly 15)")
                if r2 != 15:
                    c_issues.append(f"Round 2 has {r2} questions (Required: exactly 15)")

                # Check for empty options, invalid keys, or duplicate questions
                c.execute('SELECT id, round, order_num, question_text, option_a, option_b, option_c, option_d, correct_answer FROM questions WHERE case_id = ?', (cid,))
                q_rows = c.fetchall()
                seen_texts = {}
                for q in q_rows:
                    txt = q['question_text'].strip()
                    if not txt:
                        c_issues.append(f"Q#{q['order_num']} in Round {q['round']} has empty text")
                    if not q['option_a'] or not q['option_b'] or not q['option_c'] or not q['option_d']:
                        c_issues.append(f"Q#{q['order_num']} in Round {q['round']} missing required answer options")
                    if q['correct_answer'] not in ('A', 'B', 'C', 'D', '0', '1', '2', '3'):
                        c_issues.append(f"Q#{q['order_num']} in Round {q['round']} has invalid answer key '{q['correct_answer']}'")

                    norm_txt = txt.lower()
                    rnd = q['round']
                    key_t = f"{rnd}_{norm_txt}"
                    if key_t in seen_texts:
                        c_issues.append(f"Potential duplicate question detected in Round {rnd}: Q#{q['order_num']} matches Q#{seen_texts[key_t]}")
                    else:
                        seen_texts[key_t] = q['order_num']

                if c_issues:
                    issues.extend([f"[{cid}] {ci}" for ci in c_issues])

                validation_list.append({
                    'caseId': cid,
                    'name': cs['name'],
                    'r1Count': r1,
                    'r2Count': r2,
                    'isComplete': len(c_issues) == 0,
                    'issues': c_issues
                })

            total_cases = len(validation_list)
            is_ready = (total_cases == 15) and (len(issues) == 0)
            conn.close()
            return self.send_json(200, {
                'totalCases': total_cases,
                'requiredCases': 15,
                'isReadyForEvent': is_ready,
                'casesValidation': validation_list,
                'issues': issues
            })

        # 17. Export: Registered Teams (CSV)
        if path == '/api/admin/export/teams':
            c.execute('SELECT team_id, team_name, college_name, department, team_size, members_json, registered_at, status FROM teams ORDER BY registered_at DESC')
            rows = []
            for r in c.fetchall():
                try: mems = ', '.join(json.loads(r['members_json']))
                except: mems = ''
                rows.append({
                    'Team ID': r['team_id'],
                    'Team Name': r['team_name'],
                    'College Name': r['college_name'],
                    'Department': r['department'],
                    'Team Size': r['team_size'],
                    'Registered Members': mems,
                    'Registered At': r['registered_at'],
                    'Registration Status': r['status'],
                    'Event Status': 'STANDBY'
                })
            now_iso = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            c.execute('INSERT INTO export_logs (export_type, format, admin_id, timestamp, status, record_count) VALUES (?, ?, ?, ?, ?, ?)',
                      ('TEAMS', 'CSV', admin_id, now_iso, 'COMPLETED', len(rows)))
            c.execute('INSERT INTO audit_logs (admin_id, action, details, prev_value, new_value, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
                      (admin_id, 'EXPORT_TEAMS', f"Exported {len(rows)} registered teams as CSV (Authentication secrets excluded)", None, 'CSV_DOWNLOAD', now_iso))
            conn.commit()
            conn.close()
            fieldnames = ['Team ID', 'Team Name', 'College Name', 'Department', 'Team Size', 'Registered Members', 'Registered At', 'Registration Status', 'Event Status']
            return self.send_csv('tracex_registered_teams.csv', fieldnames, rows)

        # 18. Export: Finalized Results Matrix (CSV)
        if path == '/api/admin/export/results':
            c.execute('''
                SELECT sub.team_id, t.team_name, t.college_name, sub.case_id, sub.score_r1, sub.score_r2,
                       sub.total_score, sub.accuracy_rate, sub.violations_count, sub.evaluation_status,
                       sub.qualification_status, sub.submitted_at
                FROM submissions sub
                JOIN teams t ON sub.team_id = t.team_id
                ORDER BY sub.total_score DESC, sub.accuracy_rate DESC
            ''')
            rows = []
            for idx, r in enumerate(c.fetchall()):
                pos = f"Rank {idx+1}"
                if idx == 0: pos = '1st Place — Winner'
                elif idx == 1: pos = '2nd Place — 1st Runner Up'
                elif idx == 2: pos = '3rd Place — 2nd Runner Up'
                rows.append({
                    'Award Standing': pos,
                    'Team ID': r['team_id'],
                    'Team Name': r['team_name'],
                    'College Name': r['college_name'],
                    'Investigation Case': r['case_id'],
                    'Round 1 Score': f"{r['score_r1']} / 15",
                    'Round 2 Score': f"{r['score_r2']} / 15",
                    'Total Forensic Score': f"{r['total_score']} / 30",
                    'Accuracy Rate': f"{r['accuracy_rate']:.1f}%",
                    'Violations Recorded': r['violations_count'],
                    'Evaluation Pipeline Status': r['evaluation_status'],
                    'Authoritative Qualification Status': r['qualification_status'],
                    'Timestamp Submitted': r['submitted_at']
                })
            now_iso = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            c.execute('INSERT INTO export_logs (export_type, format, admin_id, timestamp, status, record_count) VALUES (?, ?, ?, ?, ?, ?)',
                      ('RESULTS', 'CSV', admin_id, now_iso, 'COMPLETED', len(rows)))
            c.execute('INSERT INTO audit_logs (admin_id, action, details, prev_value, new_value, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
                      (admin_id, 'EXPORT_RESULTS', f"Exported official evaluation results for {len(rows)} teams as CSV", None, 'CSV_DOWNLOAD', now_iso))
            conn.commit()
            conn.close()
            fieldnames = ['Award Standing', 'Team ID', 'Team Name', 'College Name', 'Investigation Case', 'Round 1 Score', 'Round 2 Score', 'Total Forensic Score', 'Accuracy Rate', 'Violations Recorded', 'Evaluation Pipeline Status', 'Authoritative Qualification Status', 'Timestamp Submitted']
            return self.send_csv('tracex_official_results.csv', fieldnames, rows)

        # 19. Export: Violation Logs (CSV)
        if path == '/api/admin/export/violations':
            c.execute('''
                SELECT v.id, v.team_id, t.team_name, v.violation_type, v.timestamp, v.violation_count, v.action_taken
                FROM violations v
                LEFT JOIN teams t ON v.team_id = t.team_id
                ORDER BY v.id DESC
            ''')
            rows = []
            for r in c.fetchall():
                rows.append({
                    'Log ID': f"VIO-{r['id']:04d}",
                    'Team ID': r['team_id'],
                    'Team Name': r['team_name'] or 'Unknown Team',
                    'Security Violation Type': r['violation_type'],
                    'Recorded Timestamp (UTC)': r['timestamp'],
                    'Violation Count': r['violation_count'],
                    'Automated Action Taken': r['action_taken']
                })
            now_iso = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            c.execute('INSERT INTO export_logs (export_type, format, admin_id, timestamp, status, record_count) VALUES (?, ?, ?, ?, ?, ?)',
                      ('VIOLATIONS', 'CSV', admin_id, now_iso, 'COMPLETED', len(rows)))
            c.execute('INSERT INTO audit_logs (admin_id, action, details, prev_value, new_value, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
                      (admin_id, 'EXPORT_VIOLATIONS', f"Exported {len(rows)} recorded security violation events as CSV", None, 'CSV_DOWNLOAD', now_iso))
            conn.commit()
            conn.close()
            fieldnames = ['Log ID', 'Team ID', 'Team Name', 'Security Violation Type', 'Recorded Timestamp (UTC)', 'Violation Count', 'Automated Action Taken']
            return self.send_csv('tracex_security_violations.csv', fieldnames, rows)

        # 20. Export: Final Report Data (CSV)
        if path == '/api/admin/export/report':
            c.execute('SELECT * FROM event_reports ORDER BY id DESC LIMIT 1')
            rep = c.fetchone()
            rows = []
            if rep:
                rows.append({'Section': 'EVENT DETAILS', 'Parameter': 'Event Title', 'Value': rep['title']})
                rows.append({'Section': 'EVENT DETAILS', 'Parameter': 'College Name', 'Value': rep['college_name']})
                rows.append({'Section': 'EVENT DETAILS', 'Parameter': 'Department', 'Value': rep['department_name']})
                rows.append({'Section': 'EVENT DETAILS', 'Parameter': 'Event Date', 'Value': rep['event_date']})
                rows.append({'Section': 'EVENT DETAILS', 'Parameter': 'Event Venue', 'Value': rep['event_venue']})
                rows.append({'Section': 'EVENT DETAILS', 'Parameter': 'Organizer', 'Value': rep['organizer']})
                rows.append({'Section': 'REPORT STATUS', 'Parameter': 'Status', 'Value': rep['status']})
                rows.append({'Section': 'REPORT STATUS', 'Parameter': 'Version', 'Value': f"v{rep['version']}"})
                rows.append({'Section': 'REPORT STATUS', 'Parameter': 'Published By', 'Value': rep['published_by'] or 'Unpublished (Draft)'})
                part = json.loads(rep['participation_json'])
                rows.append({'Section': 'PARTICIPATION SUMMARY', 'Parameter': 'Registered Teams', 'Value': str(part.get('registeredTeams', 0))})
                rows.append({'Section': 'PARTICIPATION SUMMARY', 'Parameter': 'Participating Teams', 'Value': str(part.get('participatingTeams', 0))})
                rows.append({'Section': 'PARTICIPATION SUMMARY', 'Parameter': 'Total Participants', 'Value': str(part.get('totalParticipants', 0))})
                rows.append({'Section': 'PARTICIPATION SUMMARY', 'Parameter': 'Completed Investigations', 'Value': str(part.get('completedInvestigations', 0))})
                rows.append({'Section': 'PARTICIPATION SUMMARY', 'Parameter': 'Disqualified Teams', 'Value': str(part.get('disqualifiedTeams', 0))})
                results = json.loads(rep['results_json'])
                for r in results:
                    rows.append({'Section': 'OFFICIAL WINNERS & AWARDS', 'Parameter': f"{r.get('teamId')} — {r.get('teamName')}", 'Value': f"{r.get('winnerPosition', '')} | {r.get('recognition', '')} (Score: {r.get('totalScore')}/30, Acc: {r.get('accuracy')})"})

            now_iso = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            c.execute('INSERT INTO export_logs (export_type, format, admin_id, timestamp, status, record_count) VALUES (?, ?, ?, ?, ?, ?)',
                      ('FINAL_REPORT', 'CSV', admin_id, now_iso, 'COMPLETED', len(rows)))
            c.execute('INSERT INTO audit_logs (admin_id, action, details, prev_value, new_value, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
                      (admin_id, 'EXPORT_REPORT_DATA', f"Exported Final Event Report data ({len(rows)} entries) as CSV", None, 'CSV_DOWNLOAD', now_iso))
            conn.commit()
            conn.close()
            fieldnames = ['Section', 'Parameter', 'Value']
            return self.send_csv('tracex_final_event_report_data.csv', fieldnames, rows)

        # 21. Export History Log
        if path == '/api/admin/export/history':
            c.execute('SELECT * FROM export_logs ORDER BY id DESC LIMIT 50')
            logs = [dict(r) for r in c.fetchall()]
            conn.close()
            return self.send_json(200, {'exportHistory': logs})

        # 22. Database Backups List
        if path == '/api/admin/backups':
            c.execute('SELECT * FROM backups ORDER BY id DESC')
            backups = []
            for r in c.fetchall():
                exists = os.path.exists(r['file_path'])
                backups.append({
                    'id': r['id'],
                    'backupId': r['backup_id'],
                    'filename': r['filename'],
                    'fileSize': r['file_size'],
                    'createdBy': r['created_by'],
                    'createdAt': r['created_at'],
                    'status': r['status'] if exists else 'MISSING_ON_DISK',
                    'details': r['details']
                })
            conn.close()
            return self.send_json(200, {'backups': backups})

        # 23. Download Database Backup File
        if path == '/api/admin/backups/download':
            bkp_id = query.get('id', [''])[0]
            c.execute('SELECT * FROM backups WHERE backup_id = ? OR id = ?', (bkp_id, bkp_id))
            b_row = c.fetchone()
            if not b_row:
                conn.close()
                return self.send_json(404, {'error': 'Backup record not found.'})

            fpath = b_row['file_path']
            if not os.path.exists(fpath):
                conn.close()
                return self.send_json(404, {'error': 'Backup file does not exist on disk.'})

            with open(fpath, 'rb') as f:
                data = f.read()

            now_iso = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            c.execute('INSERT INTO audit_logs (admin_id, action, details, prev_value, new_value, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
                      (admin_id, 'DATABASE_BACKUP_DOWNLOAD', f"Admin downloaded database backup {b_row['filename']} ({len(data)} bytes)", None, b_row['backup_id'], now_iso))
            conn.commit()
            conn.close()
            return self.send_binary(b_row['filename'], 'application/octet-stream', data)

        # 24. Database Backup Details & Integrity Stats
        if path == '/api/admin/backups/details':
            bkp_id = query.get('id', [''])[0]
            c.execute('SELECT * FROM backups WHERE backup_id = ? OR id = ?', (bkp_id, bkp_id))
            b_row = c.fetchone()
            if not b_row:
                conn.close()
                return self.send_json(404, {'error': 'Backup not found.'})

            # Check stats
            db_size = os.path.getsize(DB_FILE) if os.path.exists(DB_FILE) else 0
            c.execute("SELECT COUNT(*) FROM teams")
            teams_cnt = c.fetchone()[0]
            c.execute("SELECT COUNT(*) FROM cases")
            cases_cnt = c.fetchone()[0]
            c.execute("SELECT COUNT(*) FROM questions")
            questions_cnt = c.fetchone()[0]
            c.execute("SELECT COUNT(*) FROM submissions")
            subs_cnt = c.fetchone()[0]
            c.execute("SELECT COUNT(*) FROM audit_logs")
            audit_cnt = c.fetchone()[0]

            conn.close()
            return self.send_json(200, {
                'backup': dict(b_row),
                'liveDbSize': db_size,
                'tableCounts': {
                    'teams': teams_cnt,
                    'cases': cases_cnt,
                    'questions': questions_cnt,
                    'submissions': subs_cnt,
                    'auditLogs': audit_cnt
                }
            })

        # 25. SURREAL: Final Score Management Team List
        if path == '/api/admin/surreal/teams':
            c.execute('''
                SELECT t.team_id, t.team_name, t.college_name, t.department, t.team_size, t.members_json, t.registered_at, t.status as team_status,
                       sub.case_id, sub.score_r1, sub.score_r2, sub.total_score, sub.original_total_score,
                       sub.accuracy_rate, sub.violations_count, sub.evaluation_status, sub.qualification_status,
                       sub.score_last_modified_at, sub.score_modified_by, sub.is_score_adjusted, sub.submitted_at
                FROM teams t
                LEFT JOIN submissions sub ON UPPER(t.team_id) = UPPER(sub.team_id)
                ORDER BY sub.total_score DESC, t.team_id ASC
            ''')
            teams = []
            for r in c.fetchall():
                try:
                    members = json.loads(r['members_json'] or '[]')
                except Exception:
                    members = []
                has_sub = bool(r['case_id'])
                orig_score = r['original_total_score'] if r['original_total_score'] is not None else (r['total_score'] if r['total_score'] is not None else 0)
                final_score = r['total_score'] if r['total_score'] is not None else 0
                display_calc = final_score if r['is_score_adjusted'] else orig_score
                teams.append({
                    'teamId': r['team_id'],
                    'teamName': r['team_name'],
                    'collegeName': r['college_name'] or 'N/A',
                    'department': r['department'] or 'N/A',
                    'teamSize': r['team_size'] or 'N/A',
                    'members': members,
                    'hasSubmission': has_sub,
                    'originalCalculatedScore': display_calc,
                    'currentFinalScore': final_score,
                    'maxPossibleScore': 30,
                    'isAdjusted': bool(r['is_score_adjusted']),
                    'lastModifiedAt': r['score_last_modified_at'] or r['submitted_at'] or r['registered_at'],
                    'lastModifiedBy': r['score_modified_by'] or ('SYSTEM' if has_sub else 'N/A'),
                    'qualificationStatus': r['qualification_status'] or r['team_status'] or 'REGISTERED',
                    'evaluationStatus': r['evaluation_status'] or 'PENDING'
                })
            conn.close()
            return self.send_json(200, {
                'teams': teams,
                'maxScore': 30,
                'totalCount': len(teams)
            })

        # 26. SURREAL: Score Adjustment History
        if path == '/api/admin/surreal/history':
            target_team = query.get('teamId', query.get('team_id', ['']))[0].strip()
            if target_team:
                c.execute('''
                    SELECT id, team_id, original_score, prev_final_score, new_final_score, admin_id, reason, timestamp
                    FROM score_audit_logs
                    WHERE UPPER(team_id) = UPPER(?)
                    ORDER BY id DESC
                ''', (target_team,))
            else:
                c.execute('''
                    SELECT id, team_id, original_score, prev_final_score, new_final_score, admin_id, reason, timestamp
                    FROM score_audit_logs
                    ORDER BY id DESC LIMIT 200
                ''')
            history = []
            for r in c.fetchall():
                history.append({
                    'id': r['id'],
                    'teamId': r['team_id'],
                    'originalScore': r['original_score'],
                    'prevFinalScore': r['prev_final_score'],
                    'newFinalScore': r['new_final_score'],
                    'adminId': r['admin_id'],
                    'reason': r['reason'],
                    'timestamp': r['timestamp']
                })
            conn.close()
            return self.send_json(200, {'history': history, 'teamId': target_team})

        conn.close()
        return self.send_json(404, {'error': 'Endpoint not found.'})

    # -------------------------------------------------------------------------
    # POST Handlers
    # -------------------------------------------------------------------------
    def do_POST(self):
        path, query = self.resolve_api_path()
        body = self.read_json_body()

        conn = get_db()
        c = conn.cursor()

        # 1. Administrator Login
        if path in ('/api/admin/login', '/api/admin/auth'):
            admin_id = body.get('adminId', '').strip()
            password = body.get('password', '')

            if not admin_id or not password:
                conn.close()
                return self.send_json(400, {'error': 'Admin ID and Password are required.'})

            c.execute('SELECT * FROM admins WHERE UPPER(admin_id) = UPPER(?)', (admin_id,))
            admin = c.fetchone()
            if not admin or not verify_password(password, admin['password_hash'], admin['salt']):
                conn.close()
                return self.send_json(401, {'error': 'Invalid credentials. Access restricted to authorized personnel.'})

            token = secrets.token_hex(32)
            now = time.time()
            expires = now + (8 * 3600) # 8-hour session

            c.execute('INSERT INTO admin_sessions (token, admin_id, created_at, expires_at) VALUES (?, ?, ?, ?)',
                      (token, admin_id, now, expires))
            
            # Log admin login to audit trail
            now_iso = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            c.execute('''
                INSERT INTO audit_logs (admin_id, action, details, prev_value, new_value, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (admin_id, 'ADMIN_LOGIN', f"Successful authentication for {admin_id}", None, 'AUTHENTICATED', now_iso))

            conn.commit()
            conn.close()

            return self.send_json(200, {
                'success': True,
                'token': token,
                'admin': {
                    'adminId': admin['admin_id'],
                    'name': admin['name'],
                    'role': admin['role']
                }
            })

        # 2. Participant Team Login
        if path == '/api/teams/login':
            team_id = (body.get('teamId') or '').strip()
            pin = (body.get('pin') or body.get('pinRaw') or body.get('securityPin') or '').strip()

            if not team_id or not pin:
                conn.close()
                return self.send_json(400, {'error': 'Team ID and Security PIN are required.'})

            clean_num = team_id.lstrip('#').strip()
            c.execute('''
                SELECT * FROM teams 
                WHERE UPPER(team_id) = UPPER(?) 
                   OR CAST(registration_number AS TEXT) = ? 
                   OR CAST(registration_number AS TEXT) = ?
            ''', (team_id, team_id, clean_num))
            team = c.fetchone()
            if not team or not verify_password(pin, team['pin_hash'], team['pin_salt']):
                conn.close()
                return self.send_json(401, {'error': 'Invalid Team ID or Security PIN. Access denied.'})

            if team['status'] in ('Deactivated', 'DEACTIVATED'):
                conn.close()
                return self.send_json(403, {'error': 'This team account has been deactivated by event administration. Access denied.'})
            if team['status'] == 'Terminated':
                conn.close()
                return self.send_json(403, {'error': 'This team account has been terminated/disqualified. Access denied.'})

            # Update session connection status
            c.execute("UPDATE sessions SET connection_status = 'SECURE', updated_at = ? WHERE UPPER(team_id) = UPPER(?)", (time.time(), team['team_id']))

            # Generate participant session token
            token = secrets.token_hex(32)
            now = time.time()
            expires = now + (8 * 3600)
            c.execute('INSERT OR REPLACE INTO team_sessions (token, team_id, created_at, expires_at) VALUES (?, ?, ?, ?)',
                      (token, team['team_id'], now, expires))
            conn.commit()

            prog = get_team_progress(conn, team['team_id'])

            team_obj = {
                'teamId': team['team_id'],
                'teamName': team['team_name'],
                'collegeName': team['college_name'],
                'department': team['department'],
                'teamSize': team['team_size'],
                'status': team['status']
            }
            conn.close()
            return self.send_json(200, {'success': True, 'token': token, 'team': team_obj, 'progress': prog})

        # 2a2. Participant Case Selection Endpoint (Server-Persisted Case Assignment)
        if path == '/api/teams/select-case':
            team_id = (body.get('teamId') or '').strip()
            case_id = (body.get('caseId') or '').strip()

            if not team_id or not case_id:
                conn.close()
                return self.send_json(400, {'error': 'Team ID and Case ID are required.'})

            c.execute('SELECT * FROM teams WHERE UPPER(team_id) = UPPER(?)', (team_id,))
            team = c.fetchone()
            if not team:
                conn.close()
                return self.send_json(404, {'error': f"Team '{team_id}' not found."})

            canonical_id = team['team_id']

            if team['status'] in ('Deactivated', 'DEACTIVATED'):
                conn.close()
                return self.send_json(403, {'error': 'This team account has been deactivated. Access denied.'})
            if team['status'] == 'Terminated':
                conn.close()
                return self.send_json(403, {'error': 'This team account has been terminated. Access denied.'})

            c.execute('SELECT * FROM cases WHERE case_id = ? AND status = "ACTIVE"', (case_id,))
            case_row = c.fetchone()
            if not case_row:
                conn.close()
                return self.send_json(404, {'error': f"Investigation case '{case_id}' does not exist or is inactive."})

            # Guard: Prevent switching cases if the team has already started investigating a DIFFERENT case
            c.execute('SELECT * FROM submissions WHERE UPPER(team_id) = UPPER(?)', (canonical_id,))
            existing_sub = c.fetchone()
            if existing_sub and existing_sub['case_id'] and existing_sub['case_id'] != case_id:
                if (existing_sub['round1_answers_json'] and existing_sub['round1_answers_json'] != '{}') or \
                   (existing_sub['round2_answers_json'] and existing_sub['round2_answers_json'] != '{}') or \
                   (existing_sub['total_score'] and existing_sub['total_score'] > 0):
                    conn.close()
                    return self.send_json(400, {'error': 'Cannot change case selection after round investigation has commenced.'})

            c.execute('SELECT * FROM round_timers WHERE UPPER(team_id) = UPPER(?) AND case_id != ?', (canonical_id, case_id))
            if c.fetchone():
                conn.close()
                return self.send_json(400, {'error': 'Cannot change case selection after timer has commenced for another case.'})

            now_sec = time.time()
            c.execute('''
                INSERT INTO sessions (team_id, case_id, case_name, current_round, current_question, time_remaining, connection_status, session_status, updated_at)
                VALUES (?, ?, ?, 1, 1, '10:00', 'SECURE', 'CASE_SELECTED', ?)
                ON CONFLICT(team_id) DO UPDATE SET
                    case_id = excluded.case_id,
                    case_name = excluded.case_name,
                    session_status = CASE WHEN sessions.session_status IN ('NOT STARTED', 'PENDING SELECTION') THEN 'CASE_SELECTED' ELSE sessions.session_status END,
                    updated_at = excluded.updated_at
            ''', (canonical_id, case_id, case_row['name'], now_sec))

            # Synchronize submissions dossier
            now_iso = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            c.execute('SELECT team_id FROM submissions WHERE UPPER(team_id) = UPPER(?)', (canonical_id,))
            if not c.fetchone():
                c.execute('''
                    INSERT INTO submissions (team_id, case_id, qualification_status, submitted_at)
                    VALUES (?, ?, 'RESULTS UNDER REVIEW', ?)
                ''', (canonical_id, case_id, now_iso))
            else:
                c.execute('''
                    UPDATE submissions 
                    SET case_id = ? 
                    WHERE UPPER(team_id) = UPPER(?) AND (round1_answers_json IS NULL OR round1_answers_json = '{}')
                ''', (case_id, canonical_id))

            conn.commit()
            prog = get_team_progress(conn, canonical_id)
            conn.close()
            return self.send_json(200, {
                'success': True,
                'teamId': canonical_id,
                'caseId': case_id,
                'caseName': case_row['name'],
                'progress': prog
            })

        # 2b. Participant Team Registration Sync
        if path == '/api/teams/register':
            team_id = (body.get('teamId') or '').strip()
            team_name = (body.get('teamName') or '').strip()
            college = (body.get('collegeName') or '').strip()
            dept = (body.get('department') or '').strip()
            size = body.get('teamSize', 1)
            members = body.get('members', [])
            pin = str(body.get('pinRaw') or body.get('pin') or '').strip()

            if not team_name:
                conn.close()
                return self.send_json(400, {'error': 'Team Name is required.'})
            if not college:
                conn.close()
                return self.send_json(400, {'error': 'College Name is required.'})
            if not dept:
                conn.close()
                return self.send_json(400, {'error': 'Department is required.'})
            try:
                size = int(size)
                if size < 1 or size > 4:
                    conn.close()
                    return self.send_json(400, {'error': 'Team size must be between 1 and 4 members.'})
            except (ValueError, TypeError):
                conn.close()
                return self.send_json(400, {'error': 'Invalid team size specified.'})

            clean_members = []
            for m in (members if isinstance(members, list) else []):
                if isinstance(m, dict):
                    name_val = m.get('name') or m.get('fullName') or str(m)
                    clean_members.append(str(name_val).strip())
                elif m is not None:
                    clean_members.append(str(m).strip())

            if not clean_members:
                conn.close()
                return self.send_json(400, {'error': 'Please provide details for at least one team member.'})

            if any(not m for m in clean_members):
                conn.close()
                return self.send_json(400, {'error': 'All team member names must be non-empty.'})

            if not pin or len(pin) < 4:
                conn.close()
                return self.send_json(400, {'error': 'Security PIN must be at least 4 digits.'})

            try:
                # Immediate exclusive transaction lock to safely handle simultaneous registrations
                c.execute("BEGIN IMMEDIATE")

                # Prevent duplicate team registrations from the same institution
                c.execute('SELECT team_id FROM teams WHERE UPPER(team_name) = UPPER(?) AND UPPER(college_name) = UPPER(?)', (team_name, college))
                if c.fetchone():
                    conn.rollback()
                    conn.close()
                    return self.send_json(400, {'error': f"Duplicate registration: Team '{team_name}' from '{college}' is already registered."})

                # Authoritative sequential registration numbering (1, 2, 3...)
                c.execute('SELECT COALESCE(MAX(registration_number), 0) + 1 FROM teams')
                reg_num = c.fetchone()[0]

                if not team_id:
                    team_id = f"TX-2026-{reg_num:04d}"

                # Check if team_id already exists to prevent duplicate IDs
                c.execute('SELECT team_id FROM teams WHERE UPPER(team_id) = UPPER(?)', (team_id,))
                if c.fetchone():
                    conn.rollback()
                    conn.close()
                    return self.send_json(400, {'error': f"Team ID '{team_id}' already exists. Please choose a different ID or retry."})

                ph, ps = hash_password(pin)
                now_iso = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())

                c.execute('''
                    INSERT INTO teams (team_id, team_name, college_name, department, team_size, members_json, pin_masked, pin_hash, pin_salt, registered_at, status, registration_number)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (team_id, team_name, college, dept, size, json.dumps(clean_members), '••••••', ph, ps, now_iso, 'Registered', reg_num))

                c.execute('''
                    INSERT OR REPLACE INTO sessions (team_id, case_id, case_name, current_round, current_question, time_remaining, connection_status, session_status, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (team_id, None, 'PENDING SELECTION', 1, 1, '10:00', 'STANDBY', 'NOT STARTED', time.time()))

                # Record audit trail entry
                c.execute('''
                    INSERT INTO audit_logs (admin_id, action, details, prev_value, new_value, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', ('SYSTEM', 'TEAM_REGISTRATION', f"New team registered: {team_name} ({team_id}) - {college}", None, 'Registered', now_iso))

                c.execute('SELECT COUNT(*) as cnt FROM teams')
                total_count = c.fetchone()['cnt']

                conn.commit()
                conn.close()
                return self.send_json(200, {
                    'success': True,
                    'teamId': team_id,
                    'registrationNumber': reg_num,
                    'registrationCount': total_count
                })
            except sqlite3.IntegrityError as ie:
                conn.rollback()
                conn.close()
                return self.send_json(400, {'error': 'Registration integrity constraint error. Please check your submission.'})
            except Exception as e:
                conn.rollback()
                conn.close()
                return self.send_json(500, {'error': 'Registration failed due to a server error. Please retry.'})

        # 2c. Security Violation Logging (Deduplicated Proctoring Pipeline)
        if path == '/api/violations/log':
            team_id = (body.get('teamId') or '').strip()
            v_type = body.get('violationType') or 'TAB_SWITCH'
            v_count = int(body.get('violationCount') or 1)
            action = body.get('actionTaken') or f"Warning {v_count} of 3"
            now_iso = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())

            c.execute('''
                INSERT INTO violations (team_id, violation_type, timestamp, violation_count, action_taken)
                VALUES (?, ?, ?, ?, ?)
            ''', (team_id, v_type, now_iso, v_count, action))

            # Ensure row in submissions
            c.execute('SELECT team_id FROM submissions WHERE UPPER(team_id) = UPPER(?)', (team_id,))
            if not c.fetchone():
                c.execute('''
                    INSERT INTO submissions (team_id, case_id, violations_count, qualification_status, submitted_at)
                    VALUES (?, ?, ?, ?, ?)
                ''', (team_id, 'case-01', v_count, 'RESULTS UNDER REVIEW', now_iso))
            else:
                c.execute('UPDATE submissions SET violations_count = ? WHERE UPPER(team_id) = UPPER(?)', (v_count, team_id))

            is_disq = False
            if v_count >= 3:
                is_disq = True
                c.execute("UPDATE submissions SET qualification_status = 'DISQUALIFIED' WHERE UPPER(team_id) = UPPER(?)", (team_id,))
                c.execute("UPDATE sessions SET connection_status = 'DISCONNECTED', session_status = 'TERMINATED', updated_at = ? WHERE UPPER(team_id) = UPPER(?)", (time.time(), team_id))
                c.execute('''
                    INSERT INTO audit_logs (admin_id, action, details, prev_value, new_value, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', ('SYSTEM_PROCTOR', 'AUTOMATED_DISQUALIFICATION', f"Team {team_id} automatically terminated for exceeding 3 violations ({v_type})", None, 'DISQUALIFIED', now_iso))

            conn.commit()
            conn.close()
            return self.send_json(200, {'success': True, 'violationCount': v_count, 'isDisqualified': is_disq})

        # 2d. Early Submission of Investigation Round
        if path == '/api/round/submit-early':
            team_id = (body.get('teamId') or 'TX-2026-TEAM').strip()
            case_id = (body.get('caseId') or 'case-01').strip()
            try:
                rnd = int(body.get('round', 1))
            except (ValueError, TypeError):
                rnd = 1
            answers = body.get('answers', {})
            now_ms = int(time.time() * 1000)

            c.execute('SELECT status FROM teams WHERE UPPER(team_id) = UPPER(?)', (team_id,))
            t_row = c.fetchone()
            if not t_row:
                conn.close()
                return self.send_json(404, {'error': f"Team '{team_id}' not found."})
            if t_row['status'] in ('Deactivated', 'DEACTIVATED', 'Terminated'):
                conn.close()
                return self.send_json(403, {'error': 'Team account is deactivated or terminated. Submissions barred.'})

            timer_id = f"{team_id}_{case_id}_{rnd}"
            c.execute('''
                UPDATE round_timers
                SET is_submitted_early = 1, submitted_at_ms = ?
                WHERE id = ?
            ''', (now_ms, timer_id))

            c.execute('''
                UPDATE sessions
                SET session_status = 'SUBMITTED', updated_at = ?
                WHERE UPPER(team_id) = UPPER(?)
            ''', (time.time(), team_id))

            ans_json = json.dumps(answers)
            col = 'round1_answers_json' if rnd == 1 else 'round2_answers_json'
            c.execute(f'''
                INSERT INTO submissions (team_id, case_id, {col}, submitted_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(team_id) DO UPDATE SET
                    case_id = excluded.case_id,
                    {col} = excluded.{col},
                    submitted_at = excluded.submitted_at
            ''', (team_id, case_id, ans_json, time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())))

            # Evaluate submission against authoritative answer keys
            evaluate_team_submission(conn, team_id)

            conn.commit()

            c.execute('SELECT end_time_ms FROM round_timers WHERE id = ?', (timer_id,))
            row = c.fetchone()
            rem = max(0, int((row['end_time_ms'] - now_ms) / 1000)) if row else 0

            conn.close()
            return self.send_json(200, {'success': True, 'remainingSeconds': rem})

        # 2e. Auto-Submission on Official Timer Expiry
        if path == '/api/round/auto-submit':
            team_id = (body.get('teamId') or 'TX-2026-TEAM').strip()
            case_id = (body.get('caseId') or 'case-01').strip()
            try:
                rnd = int(body.get('round', 1))
            except (ValueError, TypeError):
                rnd = 1
            answers = body.get('answers', {})
            now_ms = int(time.time() * 1000)

            c.execute('SELECT status FROM teams WHERE UPPER(team_id) = UPPER(?)', (team_id,))
            t_row = c.fetchone()
            if not t_row:
                conn.close()
                return self.send_json(404, {'error': f"Team '{team_id}' not found."})
            if t_row['status'] in ('Deactivated', 'DEACTIVATED', 'Terminated'):
                conn.close()
                return self.send_json(403, {'error': 'Team account is deactivated or terminated. Submissions barred.'})

            timer_id = f"{team_id}_{case_id}_{rnd}"
            c.execute('''
                UPDATE round_timers
                SET is_submitted_early = 0, submitted_at_ms = ?
                WHERE id = ?
            ''', (now_ms, timer_id))

            status_str = 'ROUND 1 COMPLETED' if rnd == 1 else 'COMPLETED'
            c.execute('''
                UPDATE sessions
                SET session_status = ?, updated_at = ?
                WHERE UPPER(team_id) = UPPER(?)
            ''', (status_str, time.time(), team_id))

            ans_json = json.dumps(answers)
            col = 'round1_answers_json' if rnd == 1 else 'round2_answers_json'
            c.execute(f'''
                INSERT INTO submissions (team_id, case_id, {col}, submitted_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(team_id) DO UPDATE SET
                    case_id = excluded.case_id,
                    {col} = excluded.{col},
                    submitted_at = excluded.submitted_at
            ''', (team_id, case_id, ans_json, time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())))

            # Evaluate submission against authoritative answer keys
            evaluate_team_submission(conn, team_id)

            conn.commit()
            conn.close()
            return self.send_json(200, {'success': True, 'round': rnd, 'completed': True})

        # 2f. Participant Event Exit / Clear Workstation
        if path == '/api/participant/exit':
            team_id = (body.get('teamId') or '').strip()
            if not team_id:
                team_id = self.get_token_team() or 'TX-2026-TEAM'
            
            c.execute("UPDATE sessions SET connection_status = 'COMPLETED', session_status = 'COMPLETED', updated_at = ? WHERE UPPER(team_id) = UPPER(?)", (time.time(), team_id))
            conn.commit()
            conn.close()
            return self.send_json(200, {'success': True, 'message': 'Workstation cleared. Participant successfully completed event.'})

        # ------------------- PROTECTED ADMIN API -----------------------------
        admin_id = self.get_token_admin()
        if not admin_id:
            conn.close()
            return self.send_json(401, {'error': 'Unauthorized: Admin authentication required.'})

        # 3. Admin Logout
        if path == '/api/admin/logout':
            auth_header = self.headers.get('Authorization', '')
            token = auth_header[7:].strip() if auth_header.startswith('Bearer ') else ''
            if token:
                c.execute('DELETE FROM admin_sessions WHERE token = ?', (token,))
                conn.commit()
            conn.close()
            return self.send_json(200, {'success': True})

        # 3b. Admin Team Management: Deletion / Deactivation
        if path == '/api/admin/teams/delete':
            team_id = (body.get('teamId') or '').strip()
            reason = (body.get('reason') or 'Administrative team removal').strip()
            permanent = bool(body.get('permanent', False))

            if not team_id:
                conn.close()
                return self.send_json(400, {'error': 'Team ID is required.'})

            c.execute('SELECT * FROM teams WHERE UPPER(team_id) = UPPER(?)', (team_id,))
            team = c.fetchone()
            if not team:
                conn.close()
                return self.send_json(404, {'error': f"Team '{team_id}' not found in registry."})

            canonical_id = team['team_id']
            team_name = team['team_name']

            # Inspect database records to check participation history
            c.execute('SELECT * FROM submissions WHERE UPPER(team_id) = UPPER(?)', (canonical_id,))
            sub = c.fetchone()
            has_sub_data = bool(sub and (
                (sub['round1_answers_json'] and sub['round1_answers_json'] != '{}') or 
                (sub['round2_answers_json'] and sub['round2_answers_json'] != '{}') or 
                (sub['total_score'] and sub['total_score'] > 0) or 
                sub['evaluation_status'] == 'EVALUATED'
            ))

            c.execute('SELECT COUNT(*) as cnt FROM round_timers WHERE UPPER(team_id) = UPPER(?)', (canonical_id,))
            r_timers_cnt = c.fetchone()['cnt']

            c.execute('SELECT case_id, session_status FROM sessions WHERE UPPER(team_id) = UPPER(?)', (canonical_id,))
            s_row = c.fetchone()
            has_case_progress = bool(s_row and s_row['case_id'] and s_row['session_status'] not in ('NOT STARTED', 'PENDING SELECTION'))

            has_participation = has_sub_data or (r_timers_cnt > 0) or has_case_progress
            now_iso = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())

            # Policy: If team has participation and NOT forced permanent, soft-deactivate!
            if has_participation and not permanent:
                c.execute("UPDATE teams SET status = 'Deactivated' WHERE UPPER(team_id) = UPPER(?)", (canonical_id,))
                c.execute("UPDATE sessions SET connection_status = 'DEACTIVATED', session_status = 'DEACTIVATED', updated_at = ? WHERE UPPER(team_id) = UPPER(?)", (time.time(), canonical_id))
                c.execute("DELETE FROM team_sessions WHERE UPPER(team_id) = UPPER(?)", (canonical_id,))

                c.execute('''
                    INSERT INTO audit_logs (admin_id, action, details, prev_value, new_value, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (admin_id, 'TEAM_DEACTIVATED', f"Team {canonical_id} ({team_name}) deactivated. Historical scores and evaluation preserved. Reason: {reason}", team['status'], 'Deactivated', now_iso))

                conn.commit()
                conn.close()
                return self.send_json(200, {
                    'success': True,
                    'action': 'DEACTIVATED',
                    'message': f"Team {canonical_id} ({team_name}) has participation records and has been deactivated. Login is barred and historical competition data preserved.",
                    'teamId': canonical_id
                })
            else:
                # Permanent deletion for registration-only teams OR explicit permanent deletion
                c.execute("DELETE FROM team_sessions WHERE UPPER(team_id) = UPPER(?)", (canonical_id,))
                c.execute("DELETE FROM round_timers WHERE UPPER(team_id) = UPPER(?)", (canonical_id,))
                c.execute("DELETE FROM sessions WHERE UPPER(team_id) = UPPER(?)", (canonical_id,))
                c.execute("DELETE FROM submissions WHERE UPPER(team_id) = UPPER(?)", (canonical_id,))
                c.execute("DELETE FROM violations WHERE UPPER(team_id) = UPPER(?)", (canonical_id,))
                c.execute("DELETE FROM score_audit_logs WHERE UPPER(team_id) = UPPER(?)", (canonical_id,))
                c.execute("DELETE FROM teams WHERE UPPER(team_id) = UPPER(?)", (canonical_id,))

                c.execute('''
                    INSERT INTO audit_logs (admin_id, action, details, prev_value, new_value, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (admin_id, 'TEAM_DELETED_PERMANENT', f"Team {canonical_id} ({team_name}) permanently removed from registry. Reason: {reason}", team['status'], 'DELETED', now_iso))

                conn.commit()
                conn.close()
                return self.send_json(200, {
                    'success': True,
                    'action': 'DELETED',
                    'message': f"Team {canonical_id} ({team_name}) was permanently removed from the system.",
                    'teamId': canonical_id
                })

        # 3c. Complete Event Reset Endpoint (Protected, Verified Backup, Atomic Purge)
        if path == '/api/admin/event-reset':
            phrase = (body.get('phrase') or '').strip()
            backup_confirmed = bool(body.get('backupConfirmed', False))
            code, res_obj = execute_complete_event_reset(conn, admin_id, phrase, backup_confirmed)
            conn.close()
            return self.send_json(code, res_obj)

        # 4. Event Control State Machine
        if path == '/api/admin/event-control':
            action = body.get('action') # 'start', 'pause', 'resume', 'end', 'publish_results'
            
            if action == 'publish_results':
                c.execute("SELECT value FROM event_state WHERE key = 'settings'")
                sett_row = c.fetchone()
                settings = json.loads(sett_row['value']) if sett_row else {}
                settings['resultsPublished'] = True
                c.execute("UPDATE event_state SET value = ? WHERE key = 'settings'", (json.dumps(settings),))
                c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('results_published', '1')")
                c.execute('''
                    INSERT INTO audit_logs (admin_id, action, details, prev_value, new_value, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (admin_id, 'RESULTS_PUBLISHED', 'Published official evaluation results to candidates', None, 'PUBLISHED', time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())))
                conn.commit()
                conn.close()
                return self.send_json(200, {'success': True, 'resultsPublished': True})

            c.execute("SELECT value FROM event_state WHERE key = 'status'")
            cur_status = c.fetchone()['value']

            valid_transitions = {
                'start': (['EVENT NOT STARTED', 'EVENT PAUSED', 'EVENT ACTIVE', 'EVENT COMPLETED'], 'EVENT ACTIVE', 'ROUND 1 ACTIVE'),
                'pause': (['EVENT ACTIVE'], 'EVENT PAUSED', 'INVESTIGATION PAUSED'),
                'resume': (['EVENT PAUSED'], 'EVENT ACTIVE', 'INVESTIGATION RESUMED'),
                'end': (['EVENT ACTIVE', 'EVENT PAUSED'], 'EVENT COMPLETED', 'EVALUATION SEALED & COMPLETED'),
                'reset': (['EVENT NOT STARTED', 'EVENT PAUSED', 'EVENT ACTIVE', 'EVENT COMPLETED'], 'EVENT NOT STARTED', 'REGISTRATION & STANDBY'),
                'rearm': (['EVENT NOT STARTED', 'EVENT PAUSED', 'EVENT ACTIVE', 'EVENT COMPLETED'], 'EVENT NOT STARTED', 'REGISTRATION & STANDBY')
            }

            if action not in valid_transitions:
                conn.close()
                return self.send_json(400, {'error': f"Unknown action: {action}"})

            allowed_from, new_status, new_phase = valid_transitions[action]
            if cur_status not in allowed_from:
                conn.close()
                return self.send_json(400, {'error': f"Invalid state transition: Cannot {action} while {cur_status}."})

            # For complete event reset, enforce confirmation phrase and verified backup check
            if action in ('reset', 'rearm'):
                phrase = (body.get('phrase') or '').strip()
                backup_confirmed = bool(body.get('backupConfirmed', False))
                if phrase == 'RESET TRACEX EVENT' and backup_confirmed:
                    code, res_obj = execute_complete_event_reset(conn, admin_id, phrase, backup_confirmed)
                    conn.close()
                    return self.send_json(code, res_obj)
                else:
                    conn.close()
                    return self.send_json(400, {
                        'error': "Complete event reset requires entering the confirmation phrase 'RESET TRACEX EVENT' and confirming a verified backup exists."
                    })

            c.execute("UPDATE event_state SET value = ? WHERE key = 'status'", (new_status,))
            c.execute("UPDATE event_state SET value = ? WHERE key = 'phase'", (new_phase,))

            now_ms = int(time.time() * 1000)
            if action == 'start':
                # Establish synchronized official round start and end timestamps
                dur_r1 = 600 * 1000
                dur_r2 = 600 * 1000
                dur_eval = 300 * 1000
                c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('round', '1')")
                c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('round1_start_time', ?)", (str(now_ms),))
                c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('round1_end_time', ?)", (str(now_ms + dur_r1),))
                c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('round2_start_time', ?)", (str(now_ms + dur_r1),))
                c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('round2_end_time', ?)", (str(now_ms + dur_r1 + dur_r2),))
                c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('eval_start_time', ?)", (str(now_ms + dur_r1 + dur_r2),))
                c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('eval_end_time', ?)", (str(now_ms + dur_r1 + dur_r2 + dur_eval),))

                # Update live sessions
                c.execute("UPDATE sessions SET current_round = 1, session_status = 'ACTIVE', time_remaining = '10:00', updated_at = ?", (time.time(),))

            now_iso = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            c.execute('''
                INSERT INTO audit_logs (admin_id, action, details, prev_value, new_value, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (admin_id, f"EVENT_{action.upper()}", f"Admin executed event control action: {action.upper()}", cur_status, new_status, now_iso))

            conn.commit()
            conn.close()
            return self.send_json(200, {'success': True, 'status': new_status, 'eventStatus': new_status, 'phase': new_phase})

        # 5. Round Control Transition
        if path == '/api/admin/round-control':
            round_num = body.get('round')
            if round_num not in (1, 2, 'eval'):
                conn.close()
                return self.send_json(400, {'error': 'Invalid round specified.'})

            c.execute("UPDATE event_state SET value = ? WHERE key = 'round'", (str(round_num),))
            phase_text = f"ROUND {round_num} ACTIVE" if round_num != 'eval' else "FINAL EVALUATION PHASE"
            c.execute("UPDATE event_state SET value = ? WHERE key = 'phase'", (phase_text,))

            # Record authoritative official event-wide round start and end timestamps
            now_ms = int(time.time() * 1000)
            if round_num in (1, 2):
                dur_ms = 600 * 1000 # 10 Minutes
                c.execute(f"INSERT OR REPLACE INTO event_state (key, value) VALUES ('round{round_num}_start_time', ?)", (str(now_ms),))
                c.execute(f"INSERT OR REPLACE INTO event_state (key, value) VALUES ('round{round_num}_end_time', ?)", (str(now_ms + dur_ms),))
            elif round_num == 'eval':
                dur_ms = 300 * 1000 # 5 Minutes
                c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('eval_start_time', ?)", (str(now_ms),))
                c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('eval_end_time', ?)", (str(now_ms + dur_ms),))

            now_iso = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            c.execute('''
                INSERT INTO audit_logs (admin_id, action, details, prev_value, new_value, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (admin_id, 'ROUND_TRANSITION', f"Transitioned event to {phase_text}", None, str(round_num), now_iso))

            conn.commit()
            conn.close()
            return self.send_json(200, {'success': True, 'round': round_num, 'phase': phase_text})

        # 6. Results Publication Action
        if path == '/api/admin/results-action':
            action = body.get('action') # 'finalize', 'release', 'publish', 'withhold'
            c.execute("SELECT value FROM event_state WHERE key = 'settings'")
            settings = json.loads(c.fetchone()['value'])
            now_iso = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())

            if action == 'finalize':
                # Pre-finalization validations:
                # 1. Active teams in valid terminal session state
                # 2. Submissions exist
                # 3. All evaluated
                # 4. Calculation integrity valid
                # 5. Corrections have reason
                # 6. Overrides have reason
                # 7. No unresolved evaluation errors
                issues = []
                c.execute("SELECT COUNT(*) as cnt FROM submissions")
                total_subs = c.fetchone()['cnt']
                if total_subs == 0:
                    issues.append("No team submissions recorded in database.")

                c.execute("SELECT COUNT(*) as cnt FROM submissions WHERE evaluation_status != 'EVALUATED'")
                un_eval = c.fetchone()['cnt']
                if un_eval > 0:
                    issues.append(f"{un_eval} team submission(s) pending evaluation processing.")

                c.execute("SELECT COUNT(*) as cnt FROM submissions WHERE (score_r1 + score_r2) != total_score")
                calc_errs = c.fetchone()['cnt']
                if calc_errs > 0:
                    issues.append(f"{calc_errs} submission calculation anomalies detected.")

                if issues:
                    conn.close()
                    return self.send_json(400, {
                        'success': False,
                        'error': 'Pre-finalization validation checks failed.',
                        'issues': issues
                    })

                c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('results_finalized', '1')")
                c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('finalized_by', ?)", (admin_id,))
                c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('finalized_at', ?)", (now_iso,))

                audit_action = 'RESULTS_FINALIZED'
                details = f"All dossier scores sealed and approved by {admin_id}. Evaluation finalized."
                new_val = 'FINALIZED'
                prev_val = 'DRAFT_EVALUATION'

            elif action in ('release', 'publish'):
                c.execute("SELECT value FROM event_state WHERE key = 'results_finalized'")
                fin_row = c.fetchone()
                if not fin_row or fin_row['value'] != '1':
                    conn.close()
                    return self.send_json(400, {
                        'error': 'Results cannot be published before official finalization. Please review and finalize results first.'
                    })

                settings['resultsPublished'] = True
                c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('results_published', '1')")
                c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('published_by', ?)", (admin_id,))
                c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('published_at', ?)", (now_iso,))

                # Automatically qualify teams based on qualification threshold (e.g. >= 20/30)
                c.execute('''
                    UPDATE submissions 
                    SET qualification_status = CASE 
                        WHEN total_score >= 20 THEN 'QUALIFIED'
                        WHEN violations_count >= 3 THEN 'DISQUALIFIED'
                        ELSE 'NOT QUALIFIED'
                    END
                    WHERE qualification_status != 'DISQUALIFIED'
                ''')
                audit_action = 'RESULTS_RELEASED'
                details = f"Released official candidate qualification standings to participants by {admin_id}."
                new_val = 'PUBLISHED'
                prev_val = 'FINALIZED_UNPUBLISHED'

            elif action == 'withhold':
                settings['resultsPublished'] = False
                c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('results_published', '0')")
                audit_action = 'RESULTS_WITHHELD'
                details = f"Withheld official results from candidate views by {admin_id}."
                new_val = 'WITHHELD'
                prev_val = 'PUBLISHED'

            else:
                conn.close()
                return self.send_json(400, {'error': f"Invalid action: {action}"})

            c.execute("UPDATE event_state SET value = ? WHERE key = 'settings'", (json.dumps(settings),))
            c.execute('''
                INSERT INTO audit_logs (admin_id, action, details, prev_value, new_value, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (admin_id, audit_action, details, prev_val, new_val, now_iso))

            conn.commit()
            conn.close()
            return self.send_json(200, {
                'success': True,
                'resultsPublished': settings.get('resultsPublished', False),
                'resultsFinalized': action == 'finalize' or (fin_row['value'] == '1' if action in ('release', 'publish') else False),
                'action': action,
                'timestamp': now_iso
            })

        # 6b. Evaluation Mark Correction
        if path == '/api/admin/submissions/correct-mark':
            team_id = (body.get('teamId') or '').strip()
            question_id = (body.get('questionId') or '').strip()
            try: round_num = int(body.get('round', 1))
            except: round_num = 1
            try: order_num = int(body.get('orderNum', 1))
            except: order_num = 1
            try: new_mark = int(body.get('newMark', 0))
            except: new_mark = 0
            reason = (body.get('reason') or '').strip()

            if not team_id or not question_id or not reason:
                conn.close()
                return self.send_json(400, {'error': 'Team ID, Question ID, and a mandatory justification reason are required.'})

            if new_mark not in (0, 1):
                conn.close()
                return self.send_json(400, {'error': 'New mark must be 0 or 1.'})

            c.execute("SELECT * FROM submissions WHERE UPPER(team_id) = UPPER(?)", (team_id,))
            sub = c.fetchone()
            if not sub:
                conn.close()
                return self.send_json(404, {'error': f"Submission for team {team_id} not found."})

            try: corrections = json.loads(sub['manual_corrections_json'] or '[]')
            except: corrections = []

            # Find previous mark for this question
            prev_mark = 0
            existing_corr = None
            for idx_c, cr in enumerate(corrections):
                if cr.get('questionId') == question_id or (cr.get('round') == round_num and cr.get('orderNum') == order_num):
                    existing_corr = idx_c
                    prev_mark = cr.get('newMark', 0)
                    break

            if existing_corr is None:
                c.execute("SELECT correct_answer FROM questions WHERE id = ? OR (case_id = ? AND round = ? AND order_num = ?)",
                          (question_id, sub['case_id'], round_num, order_num))
                q_row = c.fetchone()
                corr_key = q_row['correct_answer'].strip().upper() if q_row else ''
                ans_col = sub['round1_answers_json'] if round_num == 1 else sub['round2_answers_json']
                try: ans_json = json.loads(ans_col or '{}')
                except: ans_json = {}
                if str(order_num - 1) in ans_json:
                    u_val = ans_json[str(order_num - 1)]
                elif order_num - 1 in ans_json:
                    u_val = ans_json[order_num - 1]
                elif str(order_num) in ans_json:
                    u_val = ans_json[str(order_num)]
                elif question_id in ans_json:
                    u_val = ans_json[question_id]
                else:
                    u_val = None
                idx_to_letter = {0: 'A', 1: 'B', 2: 'C', 3: 'D', '0': 'A', '1': 'B', '2': 'C', '3': 'D',
                                 'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D'}
                u_let = idx_to_letter.get(u_val, str(u_val).strip().upper() if u_val is not None else None)
                prev_mark = 1 if (u_let and u_let == corr_key) else 0

            now_iso = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            new_record = {
                'questionId': question_id,
                'round': round_num,
                'orderNum': order_num,
                'prevMark': prev_mark,
                'newMark': new_mark,
                'reason': reason,
                'adminId': admin_id,
                'timestamp': now_iso
            }

            if existing_corr is not None:
                corrections[existing_corr] = new_record
            else:
                corrections.append(new_record)

            c.execute("UPDATE submissions SET manual_corrections_json = ? WHERE UPPER(team_id) = UPPER(?)",
                      (json.dumps(corrections), team_id))

            # Recalculate submission
            evaluate_team_submission(conn, team_id)

            # Insert audit log
            c.execute('''
                INSERT INTO audit_logs (admin_id, action, details, prev_value, new_value, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                admin_id,
                'EVALUATION_MARK_CORRECTION',
                f"Team {team_id} Question {order_num} (Round {round_num}) mark adjusted from {prev_mark} to {new_mark}. Reason: {reason}",
                str(prev_mark),
                str(new_mark),
                now_iso
            ))

            conn.commit()

            c.execute("SELECT score_r1, score_r2, total_score, accuracy_rate, original_score_r1, original_score_r2, original_total_score FROM submissions WHERE UPPER(team_id) = UPPER(?)", (team_id,))
            updated_sub = c.fetchone()
            conn.close()

            return self.send_json(200, {
                'success': True,
                'teamId': team_id,
                'questionId': question_id,
                'prevMark': prev_mark,
                'newMark': new_mark,
                'scoreR1': updated_sub['score_r1'],
                'scoreR2': updated_sub['score_r2'],
                'totalScore': updated_sub['total_score'],
                'originalScoreR1': updated_sub['original_score_r1'],
                'originalScoreR2': updated_sub['original_score_r2'],
                'originalTotalScore': updated_sub['original_total_score'] if updated_sub['original_total_score'] is not None else updated_sub['total_score'],
                'accuracy': f"{updated_sub['accuracy_rate']:.1f}%",
                'reason': reason
            })

        # 6c. Official Winner Override
        if path == '/api/admin/winner-override':
            winner_team_id = (body.get('winnerTeamId') or '').strip()
            reason = (body.get('reason') or '').strip()

            if not winner_team_id or not reason:
                conn.close()
                return self.send_json(400, {'error': 'Winner Team ID and mandatory justification reason are required.'})

            c.execute('''
                SELECT sub.team_id, t.team_name, sub.total_score 
                FROM submissions sub 
                JOIN teams t ON sub.team_id = t.team_id 
                WHERE UPPER(sub.team_id) = UPPER(?)
            ''', (winner_team_id,))
            sub = c.fetchone()
            if not sub:
                conn.close()
                return self.send_json(404, {'error': f"Team {winner_team_id} not found in submissions."})

            c.execute("SELECT value FROM event_state WHERE key = 'official_winner_team_id'")
            prev_row = c.fetchone()
            prev_winner = prev_row['value'] if prev_row else ''

            now_iso = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())

            c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('official_winner_team_id', ?)", (winner_team_id,))
            c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('official_winner_reason', ?)", (reason,))
            c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('official_winner_admin_id', ?)", (admin_id,))
            c.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('official_winner_at', ?)", (now_iso,))

            # Update submissions winner declarations
            c.execute("UPDATE submissions SET winner_declaration = 'SYSTEM_CALCULATED' WHERE winner_declaration = 'OFFICIAL_OVERRIDE_WINNER'")
            c.execute("UPDATE submissions SET winner_declaration = 'OFFICIAL_OVERRIDE_WINNER', override_reason = ? WHERE UPPER(team_id) = UPPER(?)",
                      (reason, winner_team_id))

            c.execute('''
                INSERT INTO audit_logs (admin_id, action, details, prev_value, new_value, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                admin_id,
                'WINNER_OVERRIDE',
                f"Official declared winner set to Team {winner_team_id} ({sub['team_name']}). Justification: {reason}",
                prev_winner or 'SYSTEM_CALCULATED',
                winner_team_id,
                now_iso
            ))

            conn.commit()
            conn.close()
            return self.send_json(200, {
                'success': True,
                'officialWinnerTeamId': winner_team_id,
                'winnerDeclaration': 'MANUAL_OVERRIDE',
                'reason': reason,
                'adminId': admin_id,
                'timestamp': now_iso
            })

        # 7. Manual Result Override with Mandatory Reason
        if path in ('/api/admin/override-result', '/api/admin/submissions/update-status'):
            team_id = body.get('teamId')
            new_status = body.get('newStatus') or body.get('qualificationStatus') # 'QUALIFIED', 'NOT QUALIFIED', 'DISQUALIFIED'
            reason = body.get('reason', '').strip()

            if not team_id or not new_status or not reason:
                conn.close()
                return self.send_json(400, {'error': 'Team ID, new status, and a mandatory audit reason are required.'})

            c.execute('SELECT qualification_status FROM submissions WHERE team_id = ?', (team_id,))
            sub = c.fetchone()
            prev_status = sub['qualification_status'] if sub else 'UNKNOWN'

            c.execute('UPDATE submissions SET qualification_status = ? WHERE team_id = ?', (new_status, team_id))

            now_iso = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            c.execute('''
                INSERT INTO audit_logs (admin_id, action, details, prev_value, new_value, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (admin_id, 'MANUAL_RESULT_OVERRIDE', f"Team {team_id} status overridden. Reason: {reason}", prev_status, new_status, now_iso))

            conn.commit()
            conn.close()
            return self.send_json(200, {'success': True, 'teamId': team_id, 'newStatus': new_status})

        # 8. Save Event Settings
        if path == '/api/admin/settings':
            new_settings = body.get('settings', {})
            c.execute("SELECT value FROM event_state WHERE key = 'settings'")
            old_settings_json = c.fetchone()['value']

            c.execute("UPDATE event_state SET value = ? WHERE key = 'settings'", (json.dumps(new_settings),))

            now_iso = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            c.execute('''
                INSERT INTO audit_logs (admin_id, action, details, prev_value, new_value, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (admin_id, 'UPDATE_EVENT_SETTINGS', 'Administrator updated event parameters', old_settings_json, json.dumps(new_settings), now_iso))

            conn.commit()
            conn.close()
            return self.send_json(200, {'success': True, 'settings': new_settings})

        # 9. Final Report Create
        if path in ('/api/admin/report/create', '/api/admin/report'):
            live_stats = get_live_event_stats(conn)
            now_iso = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())

            title = body.get('title', 'TRACE × X — CYBER CRIME INVESTIGATION')
            college = body.get('collegeName', 'T.J.S. ENGINEERING COLLEGE')
            dept = body.get('departmentName', 'DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING')
            event_date = body.get('eventDate', time.strftime('%B %d, %Y', time.gmtime()))
            venue = body.get('eventVenue', 'Forensic Computing Lab (Lab 03 & 04), CSE Block')
            organizer = body.get('organizer', 'Department of Computer Science & Engineering in association with FOX Technical Club')
            coordinators = body.get('coordinators', 'CSE Technical Faculty & Student Forensic Committee')

            overview = {
                'introduction': body.get('introduction', 'TRACE × X is an authoritative, timed cyber crime investigation challenge designed to evaluate engineering undergraduates across real-world digital forensics, network packet analysis, and critical incident triage.'),
                'overview': body.get('overview', 'The challenge simulates an active cyber incident response wherein teams analyze forensic artifacts, dissect network captures, verify evidence integrity, and construct an unbroken chain of custody under strict time limits.'),
                'objectives': body.get('objectives', '1. Foster practical competency in digital evidence analysis and forensic methodologies.\n2. Evaluate tactical decision-making under active countdown constraints.\n3. Instill professional cyber forensic reporting standards among aspiring cybersecurity engineers.'),
                'purpose': body.get('purpose', 'To bridge academic theoretical curricula with hands-on industrial forensic triage methodologies, identifying high-aptitude talent in digital investigation and critical incident management.'),
                'highlights': body.get('highlights', 'Dual-phase timed examination (Round 1 foundational triage + Round 2 deep forensic artifacts), automated anti-cheat telemetry monitoring, and transparent evaluated decision scoring.')
            }

            participation = {
                'registeredTeams': live_stats['registeredTeams'],
                'participatingTeams': live_stats['participatingTeams'],
                'totalParticipants': live_stats['totalParticipants'],
                'completedInvestigations': live_stats['completedInvestigations'],
                'disqualifiedTeams': live_stats['disqualifiedTeams'],
                'manualOverrides': {},
                'overrideReasons': {}
            }

            structure = {
                'round1': {
                    'title': 'ROUND 1: 15 QUESTIONS — 10 MINUTES',
                    'description': 'Rapid forensic triage assessing fundamental digital evidence concepts, hash verification, chain of custody protocols, and baseline operating system artifacts under a strict 10-minute timer.'
                },
                'round2': {
                    'title': 'ROUND 2: 15 QUESTIONS — 10 MINUTES',
                    'description': 'Advanced case investigation requiring in-depth artifact reconstruction, network pcap dissection, forensic timeline mapping, and malicious actor attribution under a 10-minute countdown.'
                },
                'evaluation': {
                    'title': 'EVALUATION: 5 MINUTES',
                    'description': 'Comprehensive 5-minute automated processing window where multiple-choice and forensic telemetry submissions are scored against authoritative keys with accuracy rankings.'
                }
            }

            results = live_stats['results']

            summary = {
                'highlights': 'Exceptional participant engagement with swift triage execution in Round 1 and thorough log parsing in Round 2.',
                'challenges': 'High time pressure during complex multi-hop packet trace questions; meticulous evidence cross-referencing required.',
                'performanceSummary': f"All {live_stats['registeredTeams']} teams demonstrated disciplined forensic methodology, with leading teams achieving accuracy rates above 80%.",
                'observations': 'Participants displayed strong theoretical grounding in evidence handling; practical log analysis showed competitive performance.',
                'lessonsLearned': 'Pre-event environment briefings enhanced workstation familiarity and minimized procedural confusion.',
                'conclusion': 'TRACE × X concluded with outstanding success, meeting all pedagogy and competency objectives.',
                'recommendations': 'Recommend expanding future editions into a 3-tier structure including live memory forensics modules.',
                'acknowledgements': 'Heartfelt gratitude to the College Management, Principal, Head of Department of CSE, faculty coordinators, FOX Technical Club organizers, and all participating teams.'
            }

            organizers = {
                'preparedBy': admin_id,
                'organizerName': 'Department of Computer Science & Engineering',
                'coordinatorNames': 'Faculty & Student Coordinators',
                'facultyCoordinator': 'CSE Technical Faculty',
                'preparationDate': time.strftime('%Y-%m-%d', time.gmtime())
            }

            c.execute('''
                INSERT INTO event_reports (
                    status, version, title, college_name, department_name, event_date, event_venue, organizer, coordinators,
                    overview_json, participation_json, structure_json, results_json, summary_json, organizers_json,
                    created_at, updated_at, updated_by
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                'DRAFT', 1, title, college, dept, event_date, venue, organizer, coordinators,
                json.dumps(overview), json.dumps(participation), json.dumps(structure), json.dumps(results),
                json.dumps(summary), json.dumps(organizers), now_iso, now_iso, admin_id
            ))
            report_id = c.lastrowid

            # Snapshot in versions table
            c.execute('''
                INSERT INTO event_report_versions (report_id, version, status, data_json, saved_by, saved_at, change_summary)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (report_id, 1, 'DRAFT', json.dumps({
                'id': report_id, 'status': 'DRAFT', 'version': 1, 'title': title, 'collegeName': college, 'departmentName': dept,
                'eventDate': event_date, 'eventVenue': venue, 'organizer': organizer, 'coordinators': coordinators,
                'overview': overview, 'participation': participation, 'structure': structure, 'results': results,
                'summary': summary, 'organizers': organizers, 'updatedAt': now_iso, 'updatedBy': admin_id
            }), admin_id, now_iso, 'Initial report draft created'))

            # Audit log
            c.execute('''
                INSERT INTO audit_logs (admin_id, action, details, prev_value, new_value, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (admin_id, 'REPORT_CREATE', f"Created initial Final Event Report #{report_id} draft v1", None, 'DRAFT', now_iso))

            conn.commit()
            conn.close()
            return self.send_json(200, {'success': True, 'reportId': report_id, 'version': 1})

        # 10. Final Report Save Draft / Update
        if path == '/api/admin/report/save':
            report_id = body.get('id')
            c.execute('SELECT * FROM event_reports WHERE id = ?', (report_id,))
            current = c.fetchone()
            if not current:
                conn.close()
                return self.send_json(404, {'error': 'Report not found.'})

            if current['status'] == 'PUBLISHED':
                conn.close()
                return self.send_json(400, {'error': 'Report is PUBLISHED. Create a new revision to make changes.'})

            now_iso = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            new_version = current['version'] + 1

            title = body.get('title', current['title'])
            college = body.get('collegeName', current['college_name'])
            dept = body.get('departmentName', current['department_name'])
            event_date = body.get('eventDate', current['event_date'])
            venue = body.get('eventVenue', current['event_venue'])
            organizer = body.get('organizer', current['organizer'])
            coordinators = body.get('coordinators', current['coordinators'])
            overview = body.get('overview', json.loads(current['overview_json']))
            participation = body.get('participation', json.loads(current['participation_json']))
            structure = body.get('structure', json.loads(current['structure_json']))
            results = body.get('results', json.loads(current['results_json']))
            summary = body.get('summary', json.loads(current['summary_json']))
            organizers = body.get('organizers', json.loads(current['organizers_json']))
            change_summary = body.get('changeSummary', f"Draft updated by {admin_id}")

            # Check if any manual override was updated to log in audit
            old_part = json.loads(current['participation_json'])
            if participation.get('manualOverrides') != old_part.get('manualOverrides'):
                c.execute('''
                    INSERT INTO audit_logs (admin_id, action, details, prev_value, new_value, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (admin_id, 'REPORT_STAT_OVERRIDE', 'Participation statistics manually overridden in report', json.dumps(old_part.get('manualOverrides')), json.dumps(participation.get('manualOverrides')), now_iso))

            # Check if any result correction was made
            old_res = json.loads(current['results_json'])
            for r in results:
                tid = r.get('teamId')
                old_matching = next((x for x in old_res if x.get('teamId') == tid), None)
                if old_matching and (r.get('winnerPosition') != old_matching.get('winnerPosition') or r.get('finalStatus') != old_matching.get('finalStatus') or r.get('recognition') != old_matching.get('recognition')):
                    reason = r.get('manualCorrectionReason', 'Manual report adjustment')
                    c.execute('''
                        INSERT INTO audit_logs (admin_id, action, details, prev_value, new_value, timestamp)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (admin_id, 'REPORT_RESULT_CORRECTION', f"Result for team {tid} adjusted in report. Reason: {reason}", json.dumps(old_matching), json.dumps(r), now_iso))

            c.execute('''
                UPDATE event_reports SET
                    version = ?, title = ?, college_name = ?, department_name = ?, event_date = ?,
                    event_venue = ?, organizer = ?, coordinators = ?, overview_json = ?, participation_json = ?,
                    structure_json = ?, results_json = ?, summary_json = ?, organizers_json = ?,
                    updated_at = ?, updated_by = ?
                WHERE id = ?
            ''', (
                new_version, title, college, dept, event_date, venue, organizer, coordinators,
                json.dumps(overview), json.dumps(participation), json.dumps(structure), json.dumps(results),
                json.dumps(summary), json.dumps(organizers), now_iso, admin_id, report_id
            ))

            # Add snapshot to versions
            snapshot_data = {
                'id': report_id, 'status': current['status'], 'version': new_version, 'title': title,
                'collegeName': college, 'departmentName': dept, 'eventDate': event_date, 'eventVenue': venue,
                'organizer': organizer, 'coordinators': coordinators, 'overview': overview,
                'participation': participation, 'structure': structure, 'results': results,
                'summary': summary, 'organizers': organizers, 'updatedAt': now_iso, 'updatedBy': admin_id
            }
            c.execute('''
                INSERT INTO event_report_versions (report_id, version, status, data_json, saved_by, saved_at, change_summary)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (report_id, new_version, current['status'], json.dumps(snapshot_data), admin_id, now_iso, change_summary))

            # Audit log
            c.execute('''
                INSERT INTO audit_logs (admin_id, action, details, prev_value, new_value, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (admin_id, 'REPORT_SAVE_DRAFT', f"Saved report #{report_id} draft version {new_version}", f"v{current['version']}", f"v{new_version}", now_iso))

            conn.commit()
            conn.close()
            return self.send_json(200, {'success': True, 'version': new_version, 'updatedAt': now_iso})

        # 11. Final Report Status Transition
        if path == '/api/admin/report/status':
            report_id = body.get('id')
            target_status = body.get('targetStatus')
            valid_statuses = ['DRAFT', 'IN REVIEW', 'FINALIZED', 'PUBLISHED']
            if target_status not in valid_statuses:
                conn.close()
                return self.send_json(400, {'error': f'Invalid status. Allowed: {valid_statuses}'})

            c.execute('SELECT * FROM event_reports WHERE id = ?', (report_id,))
            current = c.fetchone()
            if not current:
                conn.close()
                return self.send_json(404, {'error': 'Report not found.'})

            prev_status = current['status']
            now_iso = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())

            pub_at = current['published_at']
            pub_by = current['published_by']
            if target_status == 'PUBLISHED':
                pub_at = now_iso
                pub_by = admin_id

            c.execute('''
                UPDATE event_reports SET
                    status = ?, published_at = ?, published_by = ?, updated_at = ?, updated_by = ?
                WHERE id = ?
            ''', (target_status, pub_at, pub_by, now_iso, admin_id, report_id))

            # Record snapshot
            c.execute('SELECT * FROM event_reports WHERE id = ?', (report_id,))
            updated_row = c.fetchone()
            snapshot_data = {
                'id': report_id, 'status': target_status, 'version': updated_row['version'],
                'title': updated_row['title'], 'collegeName': updated_row['college_name'],
                'departmentName': updated_row['department_name'], 'eventDate': updated_row['event_date'],
                'eventVenue': updated_row['event_venue'], 'organizer': updated_row['organizer'],
                'coordinators': updated_row['coordinators'], 'overview': json.loads(updated_row['overview_json']),
                'participation': json.loads(updated_row['participation_json']),
                'structure': json.loads(updated_row['structure_json']), 'results': json.loads(updated_row['results_json']),
                'summary': json.loads(updated_row['summary_json']), 'organizers': json.loads(updated_row['organizers_json']),
                'updatedAt': now_iso, 'updatedBy': admin_id, 'publishedAt': pub_at, 'publishedBy': pub_by
            }
            c.execute('''
                INSERT INTO event_report_versions (report_id, version, status, data_json, saved_by, saved_at, change_summary)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (report_id, updated_row['version'], target_status, json.dumps(snapshot_data), admin_id, now_iso, f"Status transitioned from {prev_status} to {target_status}"))

            # Audit log
            c.execute('''
                INSERT INTO audit_logs (admin_id, action, details, prev_value, new_value, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (admin_id, 'REPORT_STATUS_CHANGE', f"Report #{report_id} status changed to {target_status}", prev_status, target_status, now_iso))

            conn.commit()
            conn.close()
            return self.send_json(200, {
                'success': True,
                'status': target_status,
                'publishedAt': pub_at,
                'publishedBy': pub_by
            })

        # 12. Final Report Restore Version
        if path == '/api/admin/report/restore':
            version_id = body.get('versionId')
            c.execute('SELECT * FROM event_report_versions WHERE id = ?', (version_id,))
            ver = c.fetchone()
            if not ver:
                conn.close()
                return self.send_json(404, {'error': 'Version record not found.'})

            data = json.loads(ver['data_json'])
            report_id = ver['report_id']

            c.execute('SELECT * FROM event_reports WHERE id = ?', (report_id,))
            current = c.fetchone()
            if not current:
                conn.close()
                return self.send_json(404, {'error': 'Associated report not found.'})

            now_iso = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            new_version = current['version'] + 1

            c.execute('''
                UPDATE event_reports SET
                    version = ?, title = ?, college_name = ?, department_name = ?, event_date = ?,
                    event_venue = ?, organizer = ?, coordinators = ?, overview_json = ?, participation_json = ?,
                    structure_json = ?, results_json = ?, summary_json = ?, organizers_json = ?,
                    updated_at = ?, updated_by = ?
                WHERE id = ?
            ''', (
                new_version, data['title'], data['collegeName'], data['departmentName'], data['eventDate'],
                data['eventVenue'], data['organizer'], data['coordinators'], json.dumps(data['overview']),
                json.dumps(data['participation']), json.dumps(data['structure']), json.dumps(data['results']),
                json.dumps(data['summary']), json.dumps(data['organizers']), now_iso, admin_id, report_id
            ))

            # Record version snapshot
            c.execute('''
                INSERT INTO event_report_versions (report_id, version, status, data_json, saved_by, saved_at, change_summary)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (report_id, new_version, current['status'], json.dumps({**data, 'version': new_version, 'updatedAt': now_iso, 'updatedBy': admin_id}), admin_id, now_iso, f"Restored from version {ver['version']} (snapshot #{version_id})"))

            # Audit log
            c.execute('''
                INSERT INTO audit_logs (admin_id, action, details, prev_value, new_value, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (admin_id, 'REPORT_VERSION_RESTORE', f"Restored report #{report_id} to data from version {ver['version']}", f"v{current['version']}", f"v{new_version}", now_iso))

            conn.commit()
            conn.close()
            return self.send_json(200, {'success': True, 'version': new_version, 'restoredFrom': ver['version']})

        # 13. Final Report New Revision
        if path == '/api/admin/report/new-revision':
            report_id = body.get('id')
            c.execute('SELECT * FROM event_reports WHERE id = ?', (report_id,))
            current = c.fetchone()
            if not current:
                conn.close()
                return self.send_json(404, {'error': 'Report not found.'})

            now_iso = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            new_version = current['version'] + 1

            c.execute('''
                UPDATE event_reports SET
                    status = 'DRAFT', version = ?, updated_at = ?, updated_by = ?
                WHERE id = ?
            ''', (new_version, now_iso, admin_id, report_id))

            c.execute('''
                INSERT INTO audit_logs (admin_id, action, details, prev_value, new_value, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (admin_id, 'REPORT_NEW_REVISION', f"Initiated new draft revision v{new_version} for report #{report_id}", 'PUBLISHED', 'DRAFT', now_iso))

            conn.commit()
            conn.close()
            return self.send_json(200, {'success': True, 'version': new_version, 'status': 'DRAFT'})

        # 14. Save / Update Investigation Case
        if path == '/api/admin/cases/save':
            cid = body.get('caseId', '').strip()
            name = body.get('name', '').strip()
            summary = body.get('summary', '').strip()
            evidence = body.get('evidence', [])
            r2_evidence = body.get('round2Evidence', [])
            status = body.get('status', 'ACTIVE').upper()
            order_idx = int(body.get('orderIdx', 1))

            if not cid or not name:
                conn.close()
                return self.send_json(400, {'error': 'Case ID and Case Name are required.'})

            # Check Event Lock Status
            c.execute("SELECT value FROM event_state WHERE key = 'status'")
            st_row = c.fetchone()
            ev_status = st_row['value'] if st_row else 'EVENT NOT STARTED'
            is_active = ev_status in ('EVENT ACTIVE', 'EVENT PAUSED')

            emergency_override = body.get('emergencyOverride', False)
            emergency_reason = (body.get('emergencyReason') or '').strip()

            if is_active and (not emergency_override or not emergency_reason):
                conn.close()
                return self.send_json(403, {
                    'error': 'EVENT_LOCKED',
                    'message': 'Investigation event is currently ACTIVE. Case parameters are locked to protect live investigation integrity. Emergency modifications require explicit confirmation and a mandatory audit reason.'
                })

            now_iso = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            c.execute('SELECT * FROM cases WHERE case_id = ?', (cid,))
            existing = c.fetchone()

            if existing:
                prev_val = json.dumps({
                    'name': existing['name'],
                    'summary': existing['summary'],
                    'status': existing['status'],
                    'orderIdx': existing['order_idx']
                })
                c.execute('''
                    UPDATE cases SET
                        name = ?, summary = ?, evidence_json = ?, round2_evidence_json = ?,
                        status = ?, order_idx = ?, updated_at = ?, updated_by = ?
                    WHERE case_id = ?
                ''', (name, summary, json.dumps(evidence), json.dumps(r2_evidence), status, order_idx, now_iso, admin_id, cid))

                action_name = 'EMERGENCY_CASE_UPDATE' if is_active else 'CASE_UPDATE'
                audit_msg = f"Case {cid} updated by {admin_id}." + (f" Emergency reason: {emergency_reason}" if is_active else "")
                new_val = json.dumps({'name': name, 'summary': summary, 'status': status, 'orderIdx': order_idx})
                c.execute('''
                    INSERT INTO audit_logs (admin_id, action, details, prev_value, new_value, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (admin_id, action_name, audit_msg, prev_val, new_val, now_iso))
            else:
                c.execute('''
                    INSERT INTO cases (case_id, name, summary, evidence_json, round2_evidence_json, status, order_idx, created_at, updated_at, updated_by)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (cid, name, summary, json.dumps(evidence), json.dumps(r2_evidence), status, order_idx, now_iso, now_iso, admin_id))

                action_name = 'EMERGENCY_CASE_CREATE' if is_active else 'CASE_CREATE'
                audit_msg = f"New case {cid} ({name}) created by {admin_id}."
                c.execute('''
                    INSERT INTO audit_logs (admin_id, action, details, prev_value, new_value, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (admin_id, action_name, audit_msg, None, cid, now_iso))

            conn.commit()
            conn.close()
            return self.send_json(200, {'success': True, 'caseId': cid})

        # 15. Delete Investigation Case
        if path == '/api/admin/cases/delete':
            cid = body.get('caseId', '').strip()
            if not cid:
                conn.close()
                return self.send_json(400, {'error': 'Case ID is required.'})

            # Prevent deletion if case used in investigations
            c.execute("SELECT COUNT(*) as cnt FROM submissions WHERE case_id = ?", (cid,))
            sub_cnt = c.fetchone()['cnt']
            c.execute("SELECT COUNT(*) as cnt FROM sessions WHERE case_id = ?", (cid,))
            sess_cnt = c.fetchone()['cnt']

            if sub_cnt > 0 or sess_cnt > 0:
                conn.close()
                return self.send_json(400, {
                    'error': 'CASE_IN_USE',
                    'message': f"Cannot delete {cid}: It is currently assigned or recorded in {sub_cnt + sess_cnt} active or historical team investigations. Preserving data integrity."
                })

            # Check Event Lock Status
            c.execute("SELECT value FROM event_state WHERE key = 'status'")
            st_row = c.fetchone()
            ev_status = st_row['value'] if st_row else 'EVENT NOT STARTED'
            is_active = ev_status in ('EVENT ACTIVE', 'EVENT PAUSED')

            emergency_override = body.get('emergencyOverride', False)
            emergency_reason = (body.get('emergencyReason') or '').strip()

            if is_active and (not emergency_override or not emergency_reason):
                conn.close()
                return self.send_json(403, {
                    'error': 'EVENT_LOCKED',
                    'message': 'Cannot delete case while event is ACTIVE without explicit emergency confirmation and reason.'
                })

            now_iso = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            c.execute('DELETE FROM questions WHERE case_id = ?', (cid,))
            c.execute('DELETE FROM cases WHERE case_id = ?', (cid,))

            c.execute('''
                INSERT INTO audit_logs (admin_id, action, details, prev_value, new_value, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (admin_id, 'CASE_DELETE', f"Deleted case {cid} and all associated questions. Reason: {emergency_reason or 'Pre-event configuration'}", cid, 'DELETED', now_iso))

            conn.commit()
            conn.close()
            return self.send_json(200, {'success': True, 'deletedCaseId': cid})

        # 16. Save / Update Question
        if path == '/api/admin/questions/save':
            qid = body.get('id', '').strip()
            cid = body.get('caseId', '').strip()
            rnd = int(body.get('round', 1))
            order_num = int(body.get('orderNum', 1))
            text = body.get('text', '').strip()
            opt_a = body.get('optionA', '').strip()
            opt_b = body.get('optionB', '').strip()
            opt_c = body.get('optionC', '').strip()
            opt_d = body.get('optionD', '').strip()
            correct_ans = body.get('correctAnswer', 'A').strip().upper()
            marks = int(body.get('marks', 1))
            evidence_ref = body.get('evidenceRef', '').strip()

            # Strict Validations
            if not cid or not text:
                conn.close()
                return self.send_json(400, {'error': 'Case ID and Question Text are required.'})

            if not opt_a or not opt_b or not opt_c or not opt_d:
                conn.close()
                return self.send_json(400, {'error': 'Every question must have four answer options (Option A, B, C, and D).'})

            if correct_ans not in ('A', 'B', 'C', 'D'):
                conn.close()
                return self.send_json(400, {'error': 'Correct answer must be exactly one of Option A, B, C, or D.'})

            # Check for duplicate question text in same case and round
            ignore_dup = body.get('ignoreDuplicateWarning', False)
            c.execute('''
                SELECT id, order_num FROM questions 
                WHERE case_id = ? AND round = ? AND LOWER(TRIM(question_text)) = LOWER(TRIM(?)) AND id != ?
            ''', (cid, rnd, text, qid))
            dup_row = c.fetchone()
            if dup_row and not ignore_dup:
                conn.close()
                return self.send_json(409, {
                    'error': 'DUPLICATE_QUESTION_TEXT',
                    'message': f"Duplicate question detected! This question text matches existing Q#{dup_row['order_num']} (ID: {dup_row['id']}) in Round {rnd} for this case.",
                    'duplicateId': dup_row['id'],
                    'orderNum': dup_row['order_num']
                })

            # Check Event Lock Status
            c.execute("SELECT value FROM event_state WHERE key = 'status'")
            st_row = c.fetchone()
            ev_status = st_row['value'] if st_row else 'EVENT NOT STARTED'
            is_active = ev_status in ('EVENT ACTIVE', 'EVENT PAUSED')

            emergency_override = body.get('emergencyOverride', False)
            emergency_reason = (body.get('emergencyReason') or '').strip()

            if is_active and (not emergency_override or not emergency_reason):
                conn.close()
                return self.send_json(403, {
                    'error': 'EVENT_LOCKED',
                    'message': 'Question sets and authoritative answer keys are LOCKED while an event is in progress. Emergency edits require explicit confirmation and a mandatory reason.'
                })

            now_iso = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())

            # Generate unique ID if new
            if not qid:
                qid = f"{cid}-r{rnd}-q{order_num:02d}"
                # Ensure no ID collision
                c.execute('SELECT id FROM questions WHERE id = ?', (qid,))
                if c.fetchone():
                    qid = f"{cid}-r{rnd}-q{int(time.time())}"

            c.execute('SELECT * FROM questions WHERE id = ?', (qid,))
            existing = c.fetchone()

            if existing:
                prev_val = json.dumps({
                    'text': existing['question_text'],
                    'options': [existing['option_a'], existing['option_b'], existing['option_c'], existing['option_d']],
                    'correctAnswer': existing['correct_answer'],
                    'marks': existing['marks'],
                    'orderNum': existing['order_num']
                })
                c.execute('''
                    UPDATE questions SET
                        case_id = ?, round = ?, order_num = ?, question_text = ?,
                        option_a = ?, option_b = ?, option_c = ?, option_d = ?,
                        correct_answer = ?, marks = ?, evidence_ref = ?,
                        updated_at = ?, updated_by = ?
                    WHERE id = ?
                ''', (cid, rnd, order_num, text, opt_a, opt_b, opt_c, opt_d, correct_ans, marks, evidence_ref, now_iso, admin_id, qid))

                action_name = 'EMERGENCY_QUESTION_EDIT' if is_active else 'QUESTION_UPDATE'
                audit_msg = f"Question {qid} (Round {rnd}, Case {cid}) updated by {admin_id}." + (f" Emergency Reason: {emergency_reason}" if is_active else "")
                new_val = json.dumps({
                    'text': text,
                    'options': [opt_a, opt_b, opt_c, opt_d],
                    'correctAnswer': correct_ans,
                    'marks': marks,
                    'orderNum': order_num
                })
                c.execute('''
                    INSERT INTO audit_logs (admin_id, action, details, prev_value, new_value, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (admin_id, action_name, audit_msg, prev_val, new_val, now_iso))
            else:
                c.execute('''
                    INSERT INTO questions (id, case_id, round, order_num, question_text, option_a, option_b, option_c, option_d, correct_answer, marks, evidence_ref, created_at, updated_at, updated_by)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (qid, cid, rnd, order_num, text, opt_a, opt_b, opt_c, opt_d, correct_ans, marks, evidence_ref, now_iso, now_iso, admin_id))

                action_name = 'EMERGENCY_QUESTION_CREATE' if is_active else 'QUESTION_CREATE'
                audit_msg = f"Question {qid} added to Case {cid} Round {rnd} by {admin_id}."
                c.execute('''
                    INSERT INTO audit_logs (admin_id, action, details, prev_value, new_value, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (admin_id, action_name, audit_msg, None, qid, now_iso))

            conn.commit()
            conn.close()
            return self.send_json(200, {'success': True, 'questionId': qid})

        # 17. Delete Question
        if path == '/api/admin/questions/delete':
            qid = body.get('id', '').strip()
            if not qid:
                conn.close()
                return self.send_json(400, {'error': 'Question ID is required.'})

            # Check Event Lock Status
            c.execute("SELECT value FROM event_state WHERE key = 'status'")
            st_row = c.fetchone()
            ev_status = st_row['value'] if st_row else 'EVENT NOT STARTED'
            is_active = ev_status in ('EVENT ACTIVE', 'EVENT PAUSED')

            emergency_override = body.get('emergencyOverride', False)
            emergency_reason = (body.get('emergencyReason') or '').strip()

            if is_active and (not emergency_override or not emergency_reason):
                conn.close()
                return self.send_json(403, {
                    'error': 'EVENT_LOCKED',
                    'message': 'Cannot delete questions while an event is ACTIVE without explicit emergency confirmation and reason.'
                })

            c.execute('SELECT * FROM questions WHERE id = ?', (qid,))
            existing = c.fetchone()
            if not existing:
                conn.close()
                return self.send_json(404, {'error': 'Question not found.'})

            now_iso = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            c.execute('DELETE FROM questions WHERE id = ?', (qid,))

            action_name = 'EMERGENCY_QUESTION_DELETE' if is_active else 'QUESTION_DELETE'
            audit_msg = f"Deleted Question {qid} (Case {existing['case_id']}, Round {existing['round']}, Q#{existing['order_num']}) by {admin_id}." + (f" Emergency reason: {emergency_reason}" if is_active else "")
            c.execute('''
                INSERT INTO audit_logs (admin_id, action, details, prev_value, new_value, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (admin_id, action_name, audit_msg, qid, 'DELETED', now_iso))

            conn.commit()
            conn.close()
            return self.send_json(200, {'success': True, 'deletedId': qid})

        # 18. Reorder Questions in a Round
        if path == '/api/admin/questions/reorder':
            cid = body.get('caseId', '').strip()
            rnd = int(body.get('round', 1))
            order_list = body.get('orderList', []) # List of question IDs in order

            if not cid or not order_list:
                conn.close()
                return self.send_json(400, {'error': 'Case ID and question order list are required.'})

            # Check Event Lock Status
            c.execute("SELECT value FROM event_state WHERE key = 'status'")
            st_row = c.fetchone()
            ev_status = st_row['value'] if st_row else 'EVENT NOT STARTED'
            is_active = ev_status in ('EVENT ACTIVE', 'EVENT PAUSED')

            emergency_override = body.get('emergencyOverride', False)
            emergency_reason = (body.get('emergencyReason') or '').strip()

            if is_active and (not emergency_override or not emergency_reason):
                conn.close()
                return self.send_json(403, {
                    'error': 'EVENT_LOCKED',
                    'message': 'Questions are locked during active events. Reordering requires explicit confirmation and reason.'
                })

            now_iso = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            for idx, qid in enumerate(order_list):
                c.execute('UPDATE questions SET order_num = ?, updated_at = ?, updated_by = ? WHERE id = ? AND case_id = ? AND round = ?',
                          (idx + 1, now_iso, admin_id, qid, cid, rnd))

            action_name = 'EMERGENCY_QUESTION_REORDER' if is_active else 'QUESTION_REORDER'
            c.execute('''
                INSERT INTO audit_logs (admin_id, action, details, prev_value, new_value, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (admin_id, action_name, f"Reordered {len(order_list)} questions in Case {cid} Round {rnd} by {admin_id}", None, json.dumps(order_list), now_iso))

            conn.commit()
            conn.close()
            return self.send_json(200, {'success': True, 'reorderedCount': len(order_list)})

        # 19. Create Database Backup
        if path == '/api/admin/backups/create':
            now_iso = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            timestamp_str = time.strftime('%Y%m%d_%H%M%S', time.gmtime())
            backup_id = f"BKP-{secrets.token_hex(4).upper()}"
            filename = f"tracex_backup_{timestamp_str}.db"
            file_path = os.path.join(BACKUP_DIR, filename)

            try:
                # Perform consistent live database backup using SQLite Backup API
                src_conn = get_db()
                dest_conn = sqlite3.connect(file_path)
                src_conn.backup(dest_conn)
                dest_conn.close()
                src_conn.close()

                file_size = os.path.getsize(file_path)

                c.execute('''
                    INSERT INTO backups (backup_id, filename, file_path, file_size, created_by, created_at, status, details)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (backup_id, filename, file_path, file_size, admin_id, now_iso, 'COMPLETED', f"Consistent SQLite snapshot created by {admin_id}"))

                c.execute('''
                    INSERT INTO audit_logs (admin_id, action, details, prev_value, new_value, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (admin_id, 'DATABASE_BACKUP_CREATED', f"Created database backup {filename} ({file_size} bytes)", None, backup_id, now_iso))

                conn.commit()
                conn.close()

                return self.send_json(200, {
                    'success': True,
                    'backup': {
                        'backupId': backup_id,
                        'filename': filename,
                        'fileSize': file_size,
                        'createdAt': now_iso,
                        'createdBy': admin_id,
                        'status': 'COMPLETED'
                    }
                })
            except Exception as e:
                conn.close()
                return self.send_json(500, {'error': f"Database backup failed: {str(e)}"})

        # 20. Delete Database Backup Record & File
        if path == '/api/admin/backups/delete':
            bkp_id = body.get('backupId', '').strip()
            c.execute('SELECT * FROM backups WHERE backup_id = ? OR id = ?', (bkp_id, bkp_id))
            b_row = c.fetchone()
            if not b_row:
                conn.close()
                return self.send_json(404, {'error': 'Backup record not found.'})

            fpath = b_row['file_path']
            if os.path.exists(fpath):
                try:
                    os.remove(fpath)
                except Exception as e:
                    pass

            now_iso = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            c.execute('DELETE FROM backups WHERE id = ?', (b_row['id'],))
            c.execute('''
                INSERT INTO audit_logs (admin_id, action, details, prev_value, new_value, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (admin_id, 'DATABASE_BACKUP_DELETED', f"Deleted backup {b_row['filename']} by {admin_id}", b_row['backup_id'], 'DELETED', now_iso))

            conn.commit()
            conn.close()
            return self.send_json(200, {'success': True, 'deletedBackupId': b_row['backup_id']})

        # 21. SURREAL: Edit & Save Final Score
        if path == '/api/admin/surreal/update-score':
            team_id = str(body.get('teamId', body.get('team_id', ''))).strip()
            if not team_id:
                conn.close()
                return self.send_json(400, {'error': 'Team ID is required.'})

            c.execute("SELECT team_id, team_name FROM teams WHERE UPPER(team_id) = UPPER(?)", (team_id,))
            team_row = c.fetchone()
            if not team_row:
                conn.close()
                return self.send_json(404, {'error': f"Team '{team_id}' not found in registered teams."})

            canonical_team_id = team_row['team_id']
            team_name = team_row['team_name']

            # Score validation
            if 'newScore' not in body and 'new_score' not in body:
                conn.close()
                return self.send_json(400, {'error': 'New final score is required.'})

            raw_score = body.get('newScore') if 'newScore' in body else body.get('new_score')
            if raw_score is None:
                conn.close()
                return self.send_json(400, {'error': 'New final score cannot be null or empty.'})

            if isinstance(raw_score, bool):
                conn.close()
                return self.send_json(400, {'error': 'Score must be a valid numeric integer value.'})

            val = None
            if isinstance(raw_score, int):
                val = raw_score
            elif isinstance(raw_score, float):
                if not raw_score.is_integer():
                    conn.close()
                    return self.send_json(400, {'error': 'Invalid decimal score: final score must be a whole integer value.'})
                val = int(raw_score)
            elif isinstance(raw_score, str):
                s_val = raw_score.strip()
                if not s_val:
                    conn.close()
                    return self.send_json(400, {'error': 'Score cannot be empty.'})
                try:
                    if '.' in s_val:
                        f_val = float(s_val)
                        if not f_val.is_integer():
                            conn.close()
                            return self.send_json(400, {'error': 'Invalid decimal score: final score must be a whole integer value.'})
                        val = int(f_val)
                    else:
                        val = int(s_val)
                except ValueError:
                    conn.close()
                    return self.send_json(400, {'error': 'Invalid numeric score format. Score must be an integer between 0 and 30.'})
            else:
                conn.close()
                return self.send_json(400, {'error': 'Invalid score data type. Numeric score expected.'})

            if val < 0:
                conn.close()
                return self.send_json(400, {'error': 'Negative scores are strictly prohibited. Score cannot be less than 0.'})
            if val > 30:
                conn.close()
                return self.send_json(400, {'error': 'Score exceeds maximum possible score of 30.'})

            # Reason validation
            reason = str(body.get('reason', '')).strip()
            if not reason or len(reason) < 3:
                conn.close()
                return self.send_json(400, {'error': 'A valid reason for modifying the score is required (minimum 3 characters).'})

            # Concurrency check
            c.execute("SELECT * FROM submissions WHERE UPPER(team_id) = UPPER(?)", (canonical_team_id,))
            sub_row = c.fetchone()
            curr_final = sub_row['total_score'] if sub_row and sub_row['total_score'] is not None else 0

            expected_prev = body.get('expectedPrevScore') if 'expectedPrevScore' in body else body.get('expected_prev_score')
            if expected_prev is not None:
                try:
                    exp_val = int(expected_prev)
                    if exp_val != curr_final:
                        conn.close()
                        return self.send_json(409, {
                            'error': f"Concurrency conflict: The score for {canonical_team_id} was recently modified to {curr_final} by another administrator. Please refresh.",
                            'currentScore': curr_final
                        })
                except (ValueError, TypeError):
                    pass

            now_iso = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())

            if sub_row:
                orig_tot = sub_row['original_total_score'] if sub_row['original_total_score'] is not None else curr_final
                prev_final = curr_final
                new_accuracy = round((val / 30.0) * 100.0, 1)

                curr_qual = sub_row['qualification_status']
                if curr_qual == 'DISQUALIFIED':
                    new_qual = 'DISQUALIFIED'
                elif val >= 20:
                    new_qual = 'QUALIFIED'
                else:
                    new_qual = 'NOT QUALIFIED'

                c.execute('''
                    UPDATE submissions SET
                        total_score = ?,
                        original_total_score = ?,
                        accuracy_rate = ?,
                        score_last_modified_at = ?,
                        score_modified_by = ?,
                        is_score_adjusted = 1,
                        qualification_status = ?
                    WHERE UPPER(team_id) = UPPER(?)
                ''', (val, orig_tot, new_accuracy, now_iso, admin_id, new_qual, canonical_team_id))
            else:
                orig_tot = 0
                prev_final = 0
                new_accuracy = round((val / 30.0) * 100.0, 1)
                new_qual = 'QUALIFIED' if val >= 20 else 'NOT QUALIFIED'

                c.execute('''
                    INSERT INTO submissions (
                        team_id, case_id, score_r1, score_r2, total_score, original_total_score,
                        accuracy_rate, violations_count, evaluation_status, qualification_status,
                        score_last_modified_at, score_modified_by, is_score_adjusted, submitted_at
                    ) VALUES (?, 'UNSELECTED', 0, ?, ?, 0, ?, 0, 'EVALUATED', ?, ?, ?, 1, ?)
                ''', (canonical_team_id, val, val, new_accuracy, new_qual, now_iso, admin_id, now_iso))

            # Record append-only score audit entry
            c.execute('''
                INSERT INTO score_audit_logs (
                    team_id, original_score, prev_final_score, new_final_score, admin_id, reason, timestamp
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (canonical_team_id, orig_tot, prev_final, val, admin_id, reason, now_iso))
            audit_id = c.lastrowid

            # Also record in system administrator audit log
            c.execute('''
                INSERT INTO audit_logs (admin_id, action, details, prev_value, new_value, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (admin_id, 'SURREAL_SCORE_ADJUSTMENT', f"SURREAL: Final score adjusted for {canonical_team_id} ({team_name}) from {prev_final} to {val}. Reason: {reason}", str(prev_final), str(val), now_iso))

            conn.commit()
            conn.close()

            return self.send_json(200, {
                'success': True,
                'teamId': canonical_team_id,
                'teamName': team_name,
                'originalScore': orig_tot,
                'prevFinalScore': prev_final,
                'newFinalScore': val,
                'maxScore': 30,
                'reason': reason,
                'modifiedBy': admin_id,
                'modifiedAt': now_iso,
                'auditId': audit_id
            })

        conn.close()
        return self.send_json(404, {'error': 'Endpoint not found.'})

# -----------------------------------------------------------------------------
# Server Entry Point
# -----------------------------------------------------------------------------
def run():
    init_database()
    print(f"[TRACE × X] SQLite Database initialized at {DB_FILE}")
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, TraceXRequestHandler)
    print(f"[TRACE × X] Authoritative Engine & Web Server active on http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        httpd.server_close()

if __name__ == '__main__':
    run()
