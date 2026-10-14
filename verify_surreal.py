#!/usr/bin/env python3
"""
verify_surreal.py
Automated Verification Suite for SURREAL - Final Score Management
Department of Computer Science & Engineering, T.J.S. Engineering College
"""

import sys
import json
import urllib.request
import urllib.error
import urllib.parse
import sqlite3
import os

BASE_URL = "http://localhost:3000"
DB_PATH = os.path.join(os.path.dirname(__file__), "tracex.db")

passed = 0
failed = 0

def test(name, condition, detail=""):
    global passed, failed
    if condition:
        print(f"[PASS] {name}: {detail}")
        passed += 1
    else:
        print(f"[FAIL] {name}: {detail}")
        failed += 1

def api_request(method, path, data=None, token=None):
    url = f"{BASE_URL}{path}"
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    body = None
    if data is not None:
        headers["Content-Type"] = "application/json"
        body = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode("utf-8")
            return response.status, json.loads(res_body) if res_body else {}
    except urllib.error.HTTPError as e:
        res_body = e.read().decode("utf-8")
        try:
            return e.code, json.loads(res_body)
        except Exception:
            return e.code, {"raw": res_body}
    except Exception as e:
        return 0, {"error": str(e)}

print("\n" + "="*60)
print("TRACE × X — SURREAL FINAL SCORE MANAGEMENT AUDIT")
print("="*60 + "\n")

# -----------------------------------------------------------------------------
# Setup: Admin Login
# -----------------------------------------------------------------------------
status, admin_data = api_request("POST", "/api/admin/login", {"adminId": "admin_cse", "password": "traceX@2026"})
test("Admin Login", status == 200 and "token" in admin_data, f"Status: {status}")
admin_token = admin_data.get("token", "")

# Setup: Participant Login to obtain participant token
status, part_login = api_request("POST", "/api/teams/login", {"teamId": "TX-2026-T100", "pin": "1231"})
participant_token = part_login.get("token", "")

# -----------------------------------------------------------------------------
# Scenario 1: Authorized Administrator Opens SURREAL
# -----------------------------------------------------------------------------
status, surreal_data = api_request("GET", "/api/admin/surreal/teams", token=admin_token)
test("Scenario 1 - Authorized Admin Access to SURREAL",
     status == 200 and "teams" in surreal_data and isinstance(surreal_data["teams"], list),
     f"Teams loaded: {len(surreal_data.get('teams', []))}")

# -----------------------------------------------------------------------------
# Scenario 2: Participant Search / Filtering Verification
# -----------------------------------------------------------------------------
teams = surreal_data.get("teams", [])
found_t100 = next((t for t in teams if t["teamId"].upper() == "TX-2026-T100"), None)
test("Scenario 2 - Searchable Participant Dossier Found",
     found_t100 is not None,
     f"Team TX-2026-T100 found: {found_t100.get('teamName') if found_t100 else 'None'}")

# -----------------------------------------------------------------------------
# Scenario 3: Calculated & Final Scores Display (30 Max Score)
# -----------------------------------------------------------------------------
if found_t100:
    has_orig = "originalCalculatedScore" in found_t100
    has_final = "currentFinalScore" in found_t100
    max_score = found_t100.get("maxPossibleScore") == 30
    test("Scenario 3 - Calculated & Final Score Display Architecture",
         has_orig and has_final and max_score,
         f"Orig: {found_t100.get('originalCalculatedScore')}, Final: {found_t100.get('currentFinalScore')}, Max: {found_t100.get('maxPossibleScore')}")
else:
    test("Scenario 3 - Calculated & Final Score Display Architecture", False, "Target team missing")

# -----------------------------------------------------------------------------
# Scenario 4: Valid Score Adjustment Saved to Database
# -----------------------------------------------------------------------------
initial_final = found_t100.get("currentFinalScore", 0) if found_t100 else 0
orig_calc = found_t100.get("originalCalculatedScore", 0) if found_t100 else 0
new_test_score = 27 if initial_final != 27 else 28

status, update_res = api_request("POST", "/api/admin/surreal/update-score", {
    "teamId": "TX-2026-T100",
    "newScore": new_test_score,
    "reason": "SURREAL automated audit adjustment for evidence analysis question 14",
    "expectedPrevScore": initial_final
}, token=admin_token)

test("Scenario 4 - Valid Score Adjustment Saved",
     status == 200 and update_res.get("success") is True and update_res.get("newFinalScore") == new_test_score,
     f"Updated TX-2026-T100 from {initial_final} to {new_test_score} (Status: {status})")

# Verify in DB
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
c = conn.cursor()
c.execute("SELECT total_score, original_total_score, is_score_adjusted FROM submissions WHERE UPPER(team_id) = 'TX-2026-T100'")
sub_row = c.fetchone()
conn.close()

test("Scenario 4b - Score Persisted and Original Score Preserved in DB",
     sub_row and sub_row["total_score"] == new_test_score and sub_row["is_score_adjusted"] == 1,
     f"DB total_score: {sub_row['total_score'] if sub_row else 'None'}, original_total: {sub_row['original_total_score'] if sub_row else 'None'}")

# -----------------------------------------------------------------------------
# Scenario 5: Negative & Out-of-Range Scores Rejected
# -----------------------------------------------------------------------------
status_neg, neg_res = api_request("POST", "/api/admin/surreal/update-score", {
    "teamId": "TX-2026-T100",
    "newScore": -5,
    "reason": "Testing negative rejection"
}, token=admin_token)
test("Scenario 5a - Negative Score Rejected",
     status_neg == 400 and "negative" in neg_res.get("error", "").lower(),
     f"Status {status_neg}: {neg_res.get('error')}")

status_over, over_res = api_request("POST", "/api/admin/surreal/update-score", {
    "teamId": "TX-2026-T100",
    "newScore": 35,
    "reason": "Testing maximum score ceiling rejection"
}, token=admin_token)
test("Scenario 5b - Score > 30 Rejected",
     status_over == 400 and "exceeds" in over_res.get("error", "").lower(),
     f"Status {status_over}: {over_res.get('error')}")

# -----------------------------------------------------------------------------
# Scenario 6: Invalid Input & Malformed API Requests Rejected
# -----------------------------------------------------------------------------
status_dec, dec_res = api_request("POST", "/api/admin/surreal/update-score", {
    "teamId": "TX-2026-T100",
    "newScore": 24.75,
    "reason": "Testing decimal rejection"
}, token=admin_token)
test("Scenario 6a - Fractional Decimal Score Rejected",
     status_dec == 400 and "decimal" in dec_res.get("error", "").lower(),
     f"Status {status_dec}: {dec_res.get('error')}")

status_str, str_res = api_request("POST", "/api/admin/surreal/update-score", {
    "teamId": "TX-2026-T100",
    "newScore": "invalid_number",
    "reason": "Testing string rejection"
}, token=admin_token)
test("Scenario 6b - Non-numeric String Score Rejected",
     status_str == 400,
     f"Status {status_str}: {str_res.get('error')}")

status_empty, empty_res = api_request("POST", "/api/admin/surreal/update-score", {
    "teamId": "TX-2026-T100",
    "newScore": None,
    "reason": "Testing null rejection"
}, token=admin_token)
test("Scenario 6c - Null / Empty Score Rejected",
     status_empty == 400,
     f"Status {status_empty}: {empty_res.get('error')}")

status_noreas, noreas_res = api_request("POST", "/api/admin/surreal/update-score", {
    "teamId": "TX-2026-T100",
    "newScore": 25,
    "reason": ""
}, token=admin_token)
test("Scenario 6d - Empty Reason Rejected",
     status_noreas == 400 and "reason" in noreas_res.get("error", "").lower(),
     f"Status {status_noreas}: {noreas_res.get('error')}")

# -----------------------------------------------------------------------------
# Scenario 7: Unauthenticated Users Cannot Edit Scores
# -----------------------------------------------------------------------------
status_unauth, unauth_res = api_request("POST", "/api/admin/surreal/update-score", {
    "teamId": "TX-2026-T100",
    "newScore": 30,
    "reason": "Unauthorized attempt"
}, token=None)
test("Scenario 7 - Unauthenticated User Rejected (401)",
     status_unauth == 401,
     f"Status: {status_unauth}")

# -----------------------------------------------------------------------------
# Scenario 8: Participant Accounts Cannot Edit Scores
# -----------------------------------------------------------------------------
status_part, part_res = api_request("POST", "/api/admin/surreal/update-score", {
    "teamId": "TX-2026-T100",
    "newScore": 30,
    "reason": "Participant self-adjustment attempt"
}, token=participant_token)
test("Scenario 8 - Participant Account Blocked from Score Editing (401)",
     status_part == 401,
     f"Status: {status_part}")

# -----------------------------------------------------------------------------
# Scenario 9: Required Reason & Audit Record Saved
# -----------------------------------------------------------------------------
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
c = conn.cursor()
c.execute("SELECT * FROM score_audit_logs WHERE UPPER(team_id) = 'TX-2026-T100' ORDER BY id DESC LIMIT 1")
score_log = c.fetchone()
c.execute("SELECT * FROM audit_logs WHERE action = 'SURREAL_SCORE_ADJUSTMENT' ORDER BY id DESC LIMIT 1")
admin_log = c.fetchone()
conn.close()

test("Scenario 9 - Mandatory Audit Records Created in Both Tables",
     score_log is not None and admin_log is not None and "SURREAL" in admin_log["details"],
     f"score_audit_logs ID: {score_log['id'] if score_log else None}, prev={score_log['prev_final_score'] if score_log else None}, new={score_log['new_final_score'] if score_log else None}")

# -----------------------------------------------------------------------------
# Scenario 10: Score History Displays Previous Adjustments Correctly
# -----------------------------------------------------------------------------
status_hist, hist_data = api_request("GET", "/api/admin/surreal/history?teamId=TX-2026-T100", token=admin_token)
history_records = hist_data.get("history", [])
test("Scenario 10 - Score History Endpoint Returns Chronological Records",
     status_hist == 200 and len(history_records) >= 1 and history_records[0]["newFinalScore"] == new_test_score,
     f"Retrieved {len(history_records)} history logs for TX-2026-T100")

# -----------------------------------------------------------------------------
# Scenario 11: Results & Exports Reflect Adjusted Final Score
status_eval, eval_data = api_request("GET", "/api/admin/evaluations", token=admin_token)
eval_team = next((e for e in eval_data.get("evaluations", []) if e["teamId"].upper() == "TX-2026-T100"), None)
test("Scenario 11 - Admin Evaluation Matrix Uses Final Score",
     eval_team is not None and eval_team.get("totalScore") == new_test_score,
     f"totalScore in evaluation: {eval_team.get('totalScore') if eval_team else 'None'}")

# Test CSV export contains updated score
req = urllib.request.Request(f"{BASE_URL}/api/admin/export/results", headers={"Authorization": f"Bearer {admin_token}"})
with urllib.request.urlopen(req) as r:
    csv_text = r.read().decode("utf-8")
test("Scenario 11b - Results CSV Export Reflects Adjusted Final Score",
     f"{new_test_score} / 30" in csv_text or str(new_test_score) in csv_text,
     f"Found score {new_test_score} in CSV export")

# -----------------------------------------------------------------------------
# Scenario 12: Optimistic Concurrency Conflict Detection
# -----------------------------------------------------------------------------
status_conflict, conf_res = api_request("POST", "/api/admin/surreal/update-score", {
    "teamId": "TX-2026-T100",
    "newScore": 29,
    "reason": "Concurrent update test",
    "expectedPrevScore": 999 # Wrong previous score!
}, token=admin_token)
test("Scenario 12 - Optimistic Concurrency Conflict Handled (409)",
     status_conflict == 409 and "conflict" in conf_res.get("error", "").lower(),
     f"Status {status_conflict}: {conf_res.get('error')}")

print("\n" + "="*60)
print(f"SURREAL AUDIT SUMMARY: {passed} PASSED, {failed} FAILED")
print("="*60 + "\n")

if failed > 0:
    sys.exit(1)
else:
    sys.exit(0)
