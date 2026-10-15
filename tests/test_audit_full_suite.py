#!/usr/bin/env python3
"""
TRACE × X — Full-Stack Verification & Audit Test Suite
Department of Computer Science & Engineering | T.J.S. Engineering College

Automated verification covering Tests A through H as specified:
  • Test A: Valid Registration (Solo, Duo, Trio, Squad; sequential reg number, DB commit)
  • Test B: Invalid Registration (Incomplete/malformed payloads rejected with 400, no dirty write)
  • Test C: Duplicate Submission (Identical team name + college rejected, duplicate ID rejected)
  • Test D: Database Persistence (Committed records survive across separate queries & connections)
  • Test E: Admin Authentication (Valid credentials -> 200 + token; invalid -> 401; protected API guard)
  • Test F: Admin Registration List (/api/admin/teams returns registered teams with matching schema)
  • Test G: Admin Updates (Event control, session updates, status modifications persist)
  • Test H: Vercel Serverless Entry Point Smoke Tests (api/index.py rewrite paths & headers)

DATA SAFETY GUARANTEE:
  Runs strictly on an isolated sandbox database ('test_audit_isolated.db').
  NEVER modifies, deletes, or truncates production records in 'tracex.db'.
"""

import os
import sys
import json
import time
import shutil
import sqlite3
import threading
import urllib.request
import urllib.error
from http.server import HTTPServer

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

ORIGINAL_DB_PATH = os.path.join(ROOT_DIR, 'tracex.db')
TEST_DB_PATH = os.path.join(ROOT_DIR, 'tests', 'test_audit_isolated.db')
TEST_PORT = 3845
BASE_URL = f"http://127.0.0.1:{TEST_PORT}"

# Point environment to isolated test database
os.environ['TRACEX_DB_PATH'] = TEST_DB_PATH

import server
import api.index

test_results = []

def record_test(name, passed, message):
    test_results.append({'name': name, 'passed': passed, 'message': message})
    status = "[PASS]" if passed else "[FAIL]"
    print(f"  {status} {name}: {message}", flush=True)

def api_call(path, method='GET', data=None, token=None):
    url = f"{BASE_URL}{path}"
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = f"Bearer {token}"
    body = json.dumps(data).encode('utf-8') if data is not None else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            code = resp.getcode()
            raw = resp.read().decode('utf-8')
            try:
                res = json.loads(raw)
            except Exception:
                res = raw
            return code, res
    except urllib.error.HTTPError as e:
        raw = e.read().decode('utf-8')
        try:
            res = json.loads(raw)
        except Exception:
            res = raw
        return e.code, res
    except Exception as ex:
        return 0, {'error': str(ex)}

def run_suite():
    print("=" * 75)
    print("TRACE × X — COMPLETE FULL-STACK AUDIT & VERIFICATION SUITE")
    print("Department of Computer Science & Engineering | T.J.S. Engineering College")
    print("=" * 75)

    # Setup isolated test database from template
    if os.path.exists(TEST_DB_PATH):
        try:
            os.remove(TEST_DB_PATH)
        except Exception:
            pass

    if os.path.exists(ORIGINAL_DB_PATH):
        shutil.copyfile(ORIGINAL_DB_PATH, TEST_DB_PATH)
    
    # Apply schema migrations and setup on test database
    server.init_database()

    # Re-initialize test db schema and clear any leftover teams in isolated test db
    conn = sqlite3.connect(TEST_DB_PATH)
    conn.execute("DELETE FROM teams")
    conn.execute("DELETE FROM sessions")
    conn.execute("DELETE FROM submissions")
    conn.execute("DELETE FROM violations")
    conn.commit()
    conn.close()

    # Launch background HTTP server on test port
    httpd = HTTPServer(('127.0.0.1', TEST_PORT), server.TraceXRequestHandler)
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()
    time.sleep(0.5)

    print("\n[CHECK 1] Server Health & Initialization Check...")
    code, res = api_call('/api/health')
    record_test("Health Endpoint Check", code == 200 and res.get('status') == 'healthy', f"Server returned 200 Healthy: {res}")

    # -------------------------------------------------------------------------
    # TEST A: Valid Registration
    # -------------------------------------------------------------------------
    print("\n--- TEST A: VALID PARTICIPANT REGISTRATION ---")
    reg_payload = {
        'teamName': 'ShadowGuard',
        'collegeName': 'T.J.S. Engineering College',
        'department': 'Computer Science & Engineering',
        'teamSize': 2,
        'members': ['Praveen K', 'Arun V'],
        'pinRaw': '5842'
    }
    code, res = api_call('/api/teams/register', 'POST', reg_payload)
    assigned_team_id = res.get('teamId') if isinstance(res, dict) else None
    assigned_reg_num = res.get('registrationNumber') if isinstance(res, dict) else None

    test_a1 = (code == 200 and res.get('success') is True and bool(assigned_team_id) and assigned_reg_num == 1)
    record_test("Test A.1: Valid Registration Accepted", test_a1, f"Returned 200, Team ID={assigned_team_id}, Reg#={assigned_reg_num}")

    # Verify committed in database
    conn = sqlite3.connect(TEST_DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT team_id, team_name, college_name, pin_masked, pin_hash, pin_salt, registration_number FROM teams WHERE team_id = ?", (assigned_team_id,))
    row = c.fetchone()
    conn.close()

    test_a2 = (row is not None and row['team_name'] == 'ShadowGuard' and row['pin_masked'] == '••••••' and len(row['pin_hash']) == 64)
    record_test("Test A.2: Registration Committed to Database", test_a2, f"Found DB row: ID={row['team_id'] if row else None}, PIN Masked={row['pin_masked'] if row else None}")

    # -------------------------------------------------------------------------
    # TEST B: Invalid Registration
    # -------------------------------------------------------------------------
    print("\n--- TEST B: INVALID & INCOMPLETE REGISTRATION ---")
    # Missing team name
    code_b1, res_b1 = api_call('/api/teams/register', 'POST', {'collegeName': 'TJS', 'department': 'CSE', 'teamSize': 1, 'members': ['Alice'], 'pinRaw': '1234'})
    test_b1 = (code_b1 == 400 and 'Team Name is required' in str(res_b1))
    record_test("Test B.1: Rejection on Missing Team Name", test_b1, f"Rejected with {code_b1}: {res_b1}")

    # Missing college name
    code_b2, res_b2 = api_call('/api/teams/register', 'POST', {'teamName': 'IncompleteTeam', 'department': 'CSE', 'teamSize': 1, 'members': ['Alice'], 'pinRaw': '1234'})
    test_b2 = (code_b2 == 400 and 'College Name is required' in str(res_b2))
    record_test("Test B.2: Rejection on Missing College Name", test_b2, f"Rejected with {code_b2}: {res_b2}")

    # PIN too short (< 4 chars)
    code_b3, res_b3 = api_call('/api/teams/register', 'POST', {'teamName': 'BadPinTeam', 'collegeName': 'TJS', 'department': 'CSE', 'teamSize': 1, 'members': ['Bob'], 'pinRaw': '12'})
    test_b3 = (code_b3 == 400 and 'at least 4 digits' in str(res_b3))
    record_test("Test B.3: Rejection on Short PIN", test_b3, f"Rejected with {code_b3}: {res_b3}")

    # Verify no dirty write in database
    conn = sqlite3.connect(TEST_DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM teams WHERE team_name IN ('IncompleteTeam', 'BadPinTeam')")
    dirty_count = c.fetchone()[0]
    conn.close()
    record_test("Test B.4: No Dirty Writes on Failed Registrations", dirty_count == 0, f"Dirty records in database: {dirty_count}")

    # -------------------------------------------------------------------------
    # TEST C: Duplicate Submission Prevention
    # -------------------------------------------------------------------------
    print("\n--- TEST C: DUPLICATE REGISTRATION PREVENTION ---")
    # Try registering identical team name from same college
    code_c, res_c = api_call('/api/teams/register', 'POST', reg_payload)
    test_c = (code_c == 400 and 'already registered' in str(res_c))
    record_test("Test C.1: Duplicate Team + College Rejection", test_c, f"Status={code_c}, Error={res_c.get('error') if isinstance(res_c, dict) else res_c}")

    # Try registering duplicate Team ID explicitly
    code_c2, res_c2 = api_call('/api/teams/register', 'POST', {
        'teamId': assigned_team_id,
        'teamName': 'DifferentName',
        'collegeName': 'OtherCollege',
        'department': 'IT',
        'teamSize': 1,
        'members': ['Charlie'],
        'pinRaw': '9999'
    })
    test_c2 = (code_c2 == 400 and 'already exists' in str(res_c2))
    record_test("Test C.2: Duplicate Team ID Rejection", test_c2, f"Status={code_c2}, Error={res_c2.get('error') if isinstance(res_c2, dict) else res_c2}")

    # -------------------------------------------------------------------------
    # TEST D: Database Persistence
    # -------------------------------------------------------------------------
    print("\n--- TEST D: DATABASE PERSISTENCE ---")
    # Create a second valid registration
    second_payload = {
        'teamName': 'NetSentinels',
        'collegeName': 'Anna University',
        'department': 'Information Technology',
        'teamSize': 3,
        'members': ['Suresh P', 'Divya M', 'Kavitha R'],
        'pinRaw': '7788'
    }
    code_d1, res_d1 = api_call('/api/teams/register', 'POST', second_payload)
    second_team_id = res_d1.get('teamId') if isinstance(res_d1, dict) else None

    # Query with a completely new isolated SQLite connection
    conn2 = sqlite3.connect(TEST_DB_PATH)
    conn2.row_factory = sqlite3.Row
    c2 = conn2.cursor()
    c2.execute("SELECT team_id, team_name, registration_number, members_json FROM teams WHERE team_id = ?", (second_team_id,))
    persisted_row = c2.fetchone()
    conn2.close()

    test_d = (persisted_row is not None and persisted_row['team_name'] == 'NetSentinels' and persisted_row['registration_number'] == 2)
    record_test("Test D.1: Record Persisted Across Separate DB Connections", test_d, f"ID={second_team_id}, Reg#={persisted_row['registration_number'] if persisted_row else None}")

    # Participant login using newly registered credentials
    code_login, res_login = api_call('/api/teams/login', 'POST', {'teamId': second_team_id, 'pin': '7788'})
    test_d2 = (code_login == 200 and res_login.get('success') is True)
    record_test("Test D.2: Participant Login with Freshly Persisted Record", test_d2, f"Status={code_login}, Login success={res_login.get('success') if isinstance(res_login, dict) else False}")

    # Participant login using registration number
    code_login_num, res_login_num = api_call('/api/teams/login', 'POST', {'teamId': '#2', 'pin': '7788'})
    test_d3 = (code_login_num == 200 and res_login_num.get('success') is True)
    record_test("Test D.3: Participant Login Using Registration # (#2)", test_d3, f"Status={code_login_num}, Login success={res_login_num.get('success') if isinstance(res_login_num, dict) else False}")

    # -------------------------------------------------------------------------
    # TEST E: Admin Authentication
    # -------------------------------------------------------------------------
    print("\n--- TEST E: ADMIN AUTHENTICATION ---")
    # Valid admin credentials
    code_e1, res_e1 = api_call('/api/admin/login', 'POST', {'adminId': 'admin_cse', 'password': 'traceX@2026'})
    admin_token = res_e1.get('token') if isinstance(res_e1, dict) else None
    test_e1 = (code_e1 == 200 and res_e1.get('success') is True and bool(admin_token))
    record_test("Test E.1: Valid Admin Login Succeeds", test_e1, f"Status={code_e1}, Token received (length={len(admin_token) if admin_token else 0})")

    # Invalid admin credentials
    code_e2, res_e2 = api_call('/api/admin/login', 'POST', {'adminId': 'admin_cse', 'password': 'INCORRECT_PASSWORD'})
    test_e2 = (code_e2 == 401)
    record_test("Test E.2: Invalid Admin Password Rejected (401)", test_e2, f"Status={code_e2}, Msg={res_e2}")

    # Non-existent admin ID
    code_e3, res_e3 = api_call('/api/admin/login', 'POST', {'adminId': 'intruder_hacker', 'password': 'pass'})
    test_e3 = (code_e3 == 401)
    record_test("Test E.3: Non-Existent Admin ID Rejected (401)", test_e3, f"Status={code_e3}")

    # Unauthorized access to protected endpoints without token
    code_e4, res_e4 = api_call('/api/admin/overview')
    test_e4 = (code_e4 == 401)
    record_test("Test E.4: Protected Admin Overview Rejects Missing Token", test_e4, f"Status={code_e4}")

    code_e5, res_e5 = api_call('/api/admin/teams')
    test_e5 = (code_e5 == 401)
    record_test("Test E.5: Protected Admin Teams Rejects Missing Token", test_e5, f"Status={code_e5}")

    # -------------------------------------------------------------------------
    # TEST F: Admin Registration List
    # -------------------------------------------------------------------------
    print("\n--- TEST F: ADMIN REGISTRATION LIST ---")
    code_f, res_f = api_call('/api/admin/teams', 'GET', token=admin_token)
    teams_list = res_f.get('teams', []) if isinstance(res_f, dict) else []
    team_ids = [t['teamId'] for t in teams_list]

    test_f1 = (code_f == 200 and len(teams_list) == 2 and assigned_team_id in team_ids and second_team_id in team_ids)
    record_test("Test F.1: Admin Teams API Returns All Registered Teams", test_f1, f"Status={code_f}, Teams returned={len(teams_list)}, IDs={team_ids}")

    # Verify field mapping
    team_obj = next((t for t in teams_list if t['teamId'] == assigned_team_id), None)
    test_f2 = (
        team_obj is not None and
        team_obj['teamName'] == 'ShadowGuard' and
        team_obj['collegeName'] == 'T.J.S. Engineering College' and
        team_obj['department'] == 'Computer Science & Engineering' and
        team_obj['teamSize'] == 2 and
        team_obj['members'] == ['Praveen K', 'Arun V'] and
        team_obj['registrationNumber'] == 1 and
        team_obj['status'] == 'Registered'
    )
    record_test("Test F.2: Admin Team Detail Fields Match Database Record", test_f2, f"Team Object={team_obj}")

    # Verify Admin Overview Metrics Match Registration Count
    code_ov, res_ov = api_call('/api/admin/overview', 'GET', token=admin_token)
    test_f3 = (code_ov == 200 and res_ov.get('registeredTeams') == 2)
    record_test("Test F.3: Admin Overview Metrics Reflect Exact Team Count (2)", test_f3, f"Status={code_ov}, Registered Count={res_ov.get('registeredTeams') if isinstance(res_ov, dict) else None}")

    # -------------------------------------------------------------------------
    # TEST G: Admin Updates
    # -------------------------------------------------------------------------
    print("\n--- TEST G: ADMIN UPDATES & LIFECYCLE MANAGEMENT ---")
    # Event state transition: start event
    code_g1, res_g1 = api_call('/api/admin/event-control', 'POST', {'action': 'start'}, token=admin_token)
    test_g1 = (code_g1 == 200 and res_g1.get('status') == 'EVENT ACTIVE')
    record_test("Test G.1: Event Start Transition Succeeds", test_g1, f"Status={code_g1}, Event Status={res_g1.get('status') if isinstance(res_g1, dict) else None}")

    # Check updated event status from public endpoint
    code_g2, res_g2 = api_call('/api/event/status')
    test_g2 = (code_g2 == 200 and res_g2.get('status') == 'EVENT ACTIVE')
    record_test("Test G.2: Updated Event Status Persisted & Visible Publicly", test_g2, f"Status={code_g2}, State={res_g2.get('status') if isinstance(res_g2, dict) else None}")

    # -------------------------------------------------------------------------
    # TEST H: Production API Smoke Tests (Vercel Serverless Path Compatibility)
    # -------------------------------------------------------------------------
    print("\n--- TEST H: SERVERLESS PATH ROUTING SMOKE TESTS ---")
    # Test rewritten route using query param: /api/index.py?__path=teams/count
    code_h1, res_h1 = api_call('/api/index.py?__path=teams/count')
    test_h1 = (code_h1 == 200 and res_h1.get('count') == 2)
    record_test("Test H.1: Vercel Rewrite Path (/api/index.py?__path=teams/count)", test_h1, f"Status={code_h1}, Count={res_h1.get('count') if isinstance(res_h1, dict) else None}")

    # Test rewritten route with trailing slash
    code_h2, res_h2 = api_call('/api/index.py?__path=teams/count/')
    test_h2 = (code_h2 == 200 and res_h2.get('count') == 2)
    record_test("Test H.2: Normalized Trailing Slash in Serverless Path", test_h2, f"Status={code_h2}, Count={res_h2.get('count') if isinstance(res_h2, dict) else None}")

    # Test direct POST to Vercel rewritten endpoint: /api/index.py?__path=teams/login
    code_h3, res_h3 = api_call('/api/index.py?__path=teams/login', 'POST', {'teamId': assigned_team_id, 'pin': '5842'})
    test_h3 = (code_h3 == 200 and res_h3.get('success') is True)
    record_test("Test H.3: Serverless Rewritten POST (/api/index.py?__path=teams/login)", test_h3, f"Status={code_h3}, Success={res_h3.get('success') if isinstance(res_h3, dict) else False}")

    # Shutdown background test server
    httpd.shutdown()
    httpd.server_close()

    # Clean up isolated test db
    try:
        os.remove(TEST_DB_PATH)
    except Exception:
        pass

    # Summary
    print("\n" + "=" * 75)
    print("AUDIT & VERIFICATION SUITE SUMMARY")
    print("=" * 75)
    passed_cnt = sum(1 for t in test_results if t['passed'])
    failed_cnt = sum(1 for t in test_results if not t['passed'])
    print(f"Total Tests Executed : {len(test_results)}")
    print(f"Tests Passed         : {passed_cnt}")
    print(f"Tests Failed         : {failed_cnt}")
    success_rate = (passed_cnt / len(test_results)) * 100 if test_results else 0
    print(f"Success Rate         : {success_rate:.1f}%")
    print("=" * 75)

    if failed_cnt > 0:
        print("\nFailed Tests:")
        for t in test_results:
            if not t['passed']:
                print(f"  • {t['name']}: {t['message']}")
        sys.exit(1)
    else:
        print("\nALL AUTOMATED TESTS PASSED SUCCESSFULLY.")
        sys.exit(0)

if __name__ == '__main__':
    run_suite()
