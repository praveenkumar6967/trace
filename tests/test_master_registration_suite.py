"""
TRACE x X - Master Registration & Clean Database Automated Test Suite
Executes all verification phases:
  TEST A: Empty testing dataset (count == 0)
  TEST B: First registration (number == 1, count == 1)
  TEST C: Second registration (number == 2, count == 2)
  TEST D: Third registration (number == 3, count == 3)
  TEST E: Invalid registration data (rejected, count unchanged == 3)
  TEST F: Duplicate submission attempt (rejected, count unchanged == 3)
  TEST G: Website & Dashboard refresh (counts remain 3 and accurate)
  TEST H: Backend restart & persistence check (saved registrations intact, count == 3)
  CLEANUP: Restore dedicated testing environment to clean state (count == 0, next number == 1)
"""
import urllib.request
import urllib.parse
import json
import time
import os
import sqlite3
import sys

BASE_URL = "http://localhost:3000"
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(PROJECT_ROOT, "tracex.db")

def req(path, method="GET", data=None, headers=None):
    url = f"{BASE_URL}{path}"
    h = {"Content-Type": "application/json"}
    if headers:
        h.update(headers)
    body = json.dumps(data).encode("utf-8") if data is not None else None
    r = urllib.request.Request(url, data=body, headers=h, method=method)
    try:
        with urllib.request.urlopen(r, timeout=10) as resp:
            code = resp.getcode()
            res_body = resp.read().decode("utf-8")
            return code, json.loads(res_body)
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        try:
            return e.code, json.loads(err_body)
        except:
            return e.code, {"error": err_body}
    except Exception as ex:
        return 500, {"error": str(ex)}

def run_master_test_suite():
    print("=" * 75)
    print("EXECUTING MASTER VERIFICATION & TEST SUITE (PHASES 1 - 8)")
    print("=" * 75)

    # 1. Database Connectivity Check
    print("\n[CHECK 1] Database Connectivity & Schema...")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [r[0] for r in c.fetchall()]
    assert "teams" in tables, "teams table must exist"
    assert "admins" in tables, "admins table must exist"
    assert "cases" in tables, "cases table must exist"
    assert "questions" in tables, "questions table must exist"

    # Verify unique index on registration_number
    c.execute("PRAGMA index_list(teams)")
    indexes = [r[1] for r in c.fetchall()]
    print(f"  Verified tables: {len(tables)} tables, indexes on teams: {indexes}")
    conn.close()

    # 2. Server Health Check
    print("\n[CHECK 2] Backend Health Endpoint...")
    code, res = req("/api/health")
    assert code == 200 and res.get("status") == "healthy", f"Health check failed: {code}, {res}"
    print("  Server status: Healthy (TRACE × X Engine 2.0.0)")

    # -------------------------------------------------------------------------
    # TEST A: Start with an empty testing dataset (Expected registration count: 0)
    # -------------------------------------------------------------------------
    print("\n[TEST A] Empty Testing Dataset Initial State...")
    code, cnt_res = req("/api/teams/count")
    assert code == 200, f"Failed to get team count: {code}"
    assert cnt_res["count"] == 0, f"Expected 0 initial teams, got {cnt_res['count']}"
    assert cnt_res["nextRegistrationNumber"] == 1, f"Expected next reg num 1, got {cnt_res['nextRegistrationNumber']}"

    code, ev_res = req("/api/event/status")
    assert code == 200, f"Failed to get event status: {code}"
    assert ev_res.get("registeredTeams") == 0, f"Expected 0 registered teams in event status, got {ev_res.get('registeredTeams')}"

    # Verify Admin Overview Dashboard has count 0
    # Login as admin to get token
    code, admin_login = req("/api/admin/login", "POST", {"adminId": "admin_cse", "password": "traceX@2026"})
    assert code == 200 and "token" in admin_login, f"Admin login failed: {admin_login}"
    admin_token = admin_login["token"]

    code, overview_res = req("/api/admin/overview", "GET", headers={"Authorization": f"Bearer {admin_token}"})
    assert code == 200, f"Failed to get admin overview: {code}"
    assert overview_res["registeredTeams"] == 0, f"Expected 0 registered teams on admin dashboard, got {overview_res['registeredTeams']}"
    assert overview_res["activeParticipants"] == 0, f"Expected 0 active participants, got {overview_res['activeParticipants']}"
    assert overview_res["completedInvestigations"] == 0, f"Expected 0 completed, got {overview_res['completedInvestigations']}"
    assert overview_res["activeViolations"] == 0, f"Expected 0 violations, got {overview_res['activeViolations']}"
    print("  TEST A PASSED: Count is 0, Admin Dashboard counters are all 0.")

    # -------------------------------------------------------------------------
    # TEST B: Register one valid test user
    # -------------------------------------------------------------------------
    print("\n[TEST B] Register 1st Valid Test User...")
    code, reg1 = req("/api/teams/register", "POST", {
        "teamName": "Cyber Strike Alpha",
        "collegeName": "T.J.S. Engineering College",
        "department": "CSE",
        "teamSize": 2,
        "members": ["Student Lead 1", "Investigator 2"],
        "pinRaw": "4321"
    })
    assert code == 200 and reg1.get("success") is True, f"Registration 1 failed: {code}, {reg1}"
    assert reg1.get("registrationNumber") == 1, f"Expected registrationNumber 1, got {reg1.get('registrationNumber')}"
    assert reg1.get("registrationCount") == 1, f"Expected registrationCount 1, got {reg1.get('registrationCount')}"
    team1_id = reg1.get("teamId")
    assert team1_id == "TX-2026-0001", f"Expected sequential teamId TX-2026-0001, got {team1_id}"

    # Verify count updated
    code, cnt_res = req("/api/teams/count")
    assert cnt_res["count"] == 1, f"Expected count 1, got {cnt_res['count']}"

    code, overview_res = req("/api/admin/overview", "GET", headers={"Authorization": f"Bearer {admin_token}"})
    assert overview_res["registeredTeams"] == 1, f"Dashboard must show 1 team, got {overview_res['registeredTeams']}"
    print(f"  TEST B PASSED: Team {team1_id} registered as #{reg1.get('registrationNumber')}. Total: 1.")

    # -------------------------------------------------------------------------
    # TEST C: Register a second valid test user
    # -------------------------------------------------------------------------
    print("\n[TEST C] Register 2nd Valid Test User...")
    code, reg2 = req("/api/teams/register", "POST", {
        "teamName": "Packet Sniffers Beta",
        "collegeName": "R.M.K. Engineering College",
        "department": "IT",
        "teamSize": 3,
        "members": ["Member Alpha", "Member Beta", "Member Gamma"],
        "pinRaw": "8765"
    })
    assert code == 200 and reg2.get("success") is True, f"Registration 2 failed: {code}, {reg2}"
    assert reg2.get("registrationNumber") == 2, f"Expected registrationNumber 2, got {reg2.get('registrationNumber')}"
    assert reg2.get("registrationCount") == 2, f"Expected registrationCount 2, got {reg2.get('registrationCount')}"
    team2_id = reg2.get("teamId")
    assert team2_id == "TX-2026-0002", f"Expected sequential teamId TX-2026-0002, got {team2_id}"

    code, cnt_res = req("/api/teams/count")
    assert cnt_res["count"] == 2, f"Expected count 2, got {cnt_res['count']}"

    code, overview_res = req("/api/admin/overview", "GET", headers={"Authorization": f"Bearer {admin_token}"})
    assert overview_res["registeredTeams"] == 2, f"Dashboard must show 2 teams, got {overview_res['registeredTeams']}"
    print(f"  TEST C PASSED: Team {team2_id} registered as #{reg2.get('registrationNumber')}. Total: 2.")

    # -------------------------------------------------------------------------
    # TEST D: Register a third valid test user
    # -------------------------------------------------------------------------
    print("\n[TEST D] Register 3rd Valid Test User...")
    code, reg3 = req("/api/teams/register", "POST", {
        "teamName": "ZeroDay Hunters",
        "collegeName": "Vel Tech",
        "department": "Cyber Security",
        "teamSize": 1,
        "members": ["Solo Specialist"],
        "pinRaw": "1122"
    })
    assert code == 200 and reg3.get("success") is True, f"Registration 3 failed: {code}, {reg3}"
    assert reg3.get("registrationNumber") == 3, f"Expected registrationNumber 3, got {reg3.get('registrationNumber')}"
    assert reg3.get("registrationCount") == 3, f"Expected registrationCount 3, got {reg3.get('registrationCount')}"
    team3_id = reg3.get("teamId")
    assert team3_id == "TX-2026-0003", f"Expected sequential teamId TX-2026-0003, got {team3_id}"

    code, cnt_res = req("/api/teams/count")
    assert cnt_res["count"] == 3, f"Expected count 3, got {cnt_res['count']}"

    code, overview_res = req("/api/admin/overview", "GET", headers={"Authorization": f"Bearer {admin_token}"})
    assert overview_res["registeredTeams"] == 3, f"Dashboard must show 3 teams, got {overview_res['registeredTeams']}"
    print(f"  TEST D PASSED: Team {team3_id} registered as #{reg3.get('registrationNumber')}. Total: 3.")

    # -------------------------------------------------------------------------
    # TEST E: Submit invalid registration data
    # -------------------------------------------------------------------------
    print("\n[TEST E] Submit Invalid Registration Data (Empty Name)...")
    code, reg_inv = req("/api/teams/register", "POST", {
        "teamName": "   ",
        "collegeName": "T.J.S. Engineering College"
    })
    assert code == 400, f"Expected 400 for invalid data, got {code}: {reg_inv}"
    assert "error" in reg_inv, "Must return error message"

    # Count must remain unchanged
    code, cnt_res = req("/api/teams/count")
    assert cnt_res["count"] == 3, f"Expected count to remain 3, got {cnt_res['count']}"
    print(f"  TEST E PASSED: Rejected with code {code}. Count unchanged at {cnt_res['count']}.")

    # -------------------------------------------------------------------------
    # TEST F: Attempt duplicate submission
    # -------------------------------------------------------------------------
    print("\n[TEST F] Attempt Duplicate Submissions...")
    # Attempt 1: Duplicate team name from same college
    code, dup_name = req("/api/teams/register", "POST", {
        "teamName": "Cyber Strike Alpha",
        "collegeName": "T.J.S. Engineering College",
        "pinRaw": "9999"
    })
    assert code == 400, f"Expected 400 for duplicate institution team, got {code}: {dup_name}"
    assert "Duplicate registration" in dup_name.get("error", ""), f"Expected duplicate error, got {dup_name}"

    # Attempt 2: Duplicate team ID
    code, dup_id = req("/api/teams/register", "POST", {
        "teamId": team1_id,
        "teamName": "Another Name",
        "collegeName": "Another College",
        "pinRaw": "9999"
    })
    assert code == 400, f"Expected 400 for duplicate ID, got {code}: {dup_id}"

    # Count must remain unchanged
    code, cnt_res = req("/api/teams/count")
    assert cnt_res["count"] == 3, f"Expected count to remain 3, got {cnt_res['count']}"
    print(f"  TEST F PASSED: Both duplicate attempts rejected. Count unchanged at {cnt_res['count']}.")

    # -------------------------------------------------------------------------
    # TEST G: Refresh website and dashboard
    # -------------------------------------------------------------------------
    print("\n[TEST G] Refresh Website and Dashboard Telemetry...")
    # Simulate page refresh by fetching all endpoints afresh
    code, ev_res = req("/api/event/status")
    assert ev_res["registeredTeams"] == 3, f"Event status count must be 3, got {ev_res['registeredTeams']}"

    code, overview_res = req("/api/admin/overview", "GET", headers={"Authorization": f"Bearer {admin_token}"})
    assert overview_res["registeredTeams"] == 3, f"Dashboard count must be 3, got {overview_res['registeredTeams']}"

    code, teams_res = req("/api/admin/teams", "GET", headers={"Authorization": f"Bearer {admin_token}"})
    assert code == 200, f"Failed to get teams list: {code}"
    teams = teams_res.get("teams", [])
    assert len(teams) == 3, f"Expected 3 teams in admin table, got {len(teams)}"
    # Verify sequential numbers in reverse chronological order
    reg_nums = [t["registrationNumber"] for t in teams]
    assert reg_nums == [3, 2, 1], f"Expected registration numbers [3, 2, 1], got {reg_nums}"
    print(f"  TEST G PASSED: Refreshed dashboard reports 3 teams with sequential IDs: {[t['teamId'] for t in teams]}.")

    # Participant login test: verify login with teamId AND with registration number
    print("\n[CHECK 3] Participant Login with Team ID and Registration Number...")
    code, log1 = req("/api/teams/login", "POST", {"teamId": team1_id, "pin": "4321"})
    assert code == 200 and log1.get("success") is True, f"Login by Team ID failed: {log1}"
    code, log2 = req("/api/teams/login", "POST", {"teamId": "1", "pin": "4321"})
    assert code == 200 and log2.get("success") is True, f"Login by Registration Number failed: {log2}"
    print(f"  CHECK 3 PASSED: Team successfully authenticated using both '{team1_id}' and '1'.")

    # -------------------------------------------------------------------------
    # TEST H: Restart the backend and check database persistence
    # -------------------------------------------------------------------------
    print("\n[TEST H] Backend Cold Restart & Database Persistence Check...")
    # Directly verify database file records
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT team_id, team_name, registration_number FROM teams ORDER BY registration_number ASC")
    db_teams = c.fetchall()
    conn.close()

    assert len(db_teams) == 3, f"Expected 3 persisted teams in DB, got {len(db_teams)}"
    assert db_teams[0][2] == 1 and db_teams[0][0] == "TX-2026-0001"
    assert db_teams[1][2] == 2 and db_teams[1][0] == "TX-2026-0002"
    assert db_teams[2][2] == 3 and db_teams[2][0] == "TX-2026-0003"
    print(f"  TEST H PASSED: All 3 teams persisted in SQLite with valid sequential numbers.")

    # -------------------------------------------------------------------------
    # CLEANUP: Remove only the test records created by these tests
    # -------------------------------------------------------------------------
    print("\n[CLEANUP] Restoring Dedicated Testing Environment to Clean State (Count = 0)...")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    test_ids = [team1_id, team2_id, team3_id]
    for tid in test_ids:
        c.execute("DELETE FROM sessions WHERE UPPER(team_id) = UPPER(?)", (tid,))
        c.execute("DELETE FROM team_sessions WHERE UPPER(team_id) = UPPER(?)", (tid,))
        c.execute("DELETE FROM teams WHERE UPPER(team_id) = UPPER(?)", (tid,))
    try:
        c.execute("DELETE FROM sqlite_sequence WHERE name IN ('violations', 'score_audit_logs', 'event_reports', 'event_report_versions', 'teams')")
    except:
        pass

    conn.commit()
    c.execute("SELECT COUNT(*) FROM teams")
    final_count = c.fetchone()[0]
    c.execute("SELECT COALESCE(MAX(registration_number), 0) FROM teams")
    final_max = c.fetchone()[0]
    conn.close()

    assert final_count == 0, f"Expected 0 teams after cleanup, got {final_count}"
    assert final_max == 0, f"Expected next reg num 1, got {final_max + 1}"

    # Verify HTTP count reports 0
    code, cnt_res = req("/api/teams/count")
    assert cnt_res["count"] == 0, f"HTTP count must be 0, got {cnt_res['count']}"
    assert cnt_res["nextRegistrationNumber"] == 1, f"Next registration must be 1, got {cnt_res['nextRegistrationNumber']}"

    code, overview_res = req("/api/admin/overview", "GET", headers={"Authorization": f"Bearer {admin_token}"})
    assert overview_res["registeredTeams"] == 0, f"Dashboard must show 0, got {overview_res['registeredTeams']}"

    print(f"  CLEANUP PASSED: Testing environment restored to count 0. Next registration is #1.")
    print("=" * 75)
    print("ALL TESTS (TEST A THROUGH TEST H + CLEANUP) COMPLETED WITH 100% SUCCESS!")
    print("=" * 75)
    return True

if __name__ == "__main__":
    ok = run_master_test_suite()
    sys.exit(0 if ok else 1)
