"""
TRACE x X - Comprehensive Automated Regression Test Suite
Validates all 26 points from the specification against the live server.
"""

import urllib.request
import urllib.parse
import json
import time
import sys

BASE_URL = "http://localhost:3000"

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
            try:
                parsed = json.loads(res_body)
            except Exception:
                parsed = res_body
            return code, parsed
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        try:
            parsed = json.loads(err_body)
        except Exception:
            parsed = err_body
        return e.code, parsed
    except Exception as ex:
        return 500, {"error": str(ex)}

def run_tests():
    results = {}
    print("=" * 70)
    print("STARTING TRACE × X AUTOMATED REGRESSION SUITE (26 POINTS)")
    print("=" * 70)

    # 1. Register Team A
    ts = int(time.time() * 1000)
    team_a_id = f"TX-REG-A-{ts}"
    code, res = req("/api/teams/register", "POST", {
        "teamId": team_a_id,
        "teamName": "Team Alpha Cyber",
        "collegeName": "College of Engg",
        "department": "CSE",
        "teamSize": 2,
        "members": [{"name": "Alice", "email": "a@cse.edu", "phone": "9998887771"}],
        "pinRaw": "1111"
    })
    results[1] = (code == 200 and res.get("success") is True, f"Status: {code}, res: {res}")
    print(f"Test 1 - Register Team A ({team_a_id}): {'PASS' if results[1][0] else 'FAIL'}")

    # 2. Register Team B
    team_b_id = f"TX-REG-B-{ts}"
    code, res = req("/api/teams/register", "POST", {
        "teamId": team_b_id,
        "teamName": "Team Bravo Forensics",
        "collegeName": "College of Tech",
        "department": "IT",
        "teamSize": 2,
        "members": [{"name": "Bob", "email": "b@it.edu", "phone": "9998887772"}],
        "pinRaw": "2222"
    })
    results[2] = (code == 200 and res.get("success") is True, f"Status: {code}, res: {res}")
    print(f"Test 2 - Register Team B ({team_b_id}): {'PASS' if results[2][0] else 'FAIL'}")

    # 3. Log in as Team A and select Case 2
    code, login_a = req("/api/teams/login", "POST", {"teamId": team_a_id, "pin": "1111"})
    token_a = login_a.get("token")
    code_sel, res_sel_a = req("/api/teams/select-case", "POST", {"teamId": team_a_id, "caseId": "case-02"}, {"Authorization": f"Bearer {token_a}"})
    results[3] = (code == 200 and code_sel == 200 and res_sel_a.get("success") is True, f"Login: {code}, Select: {code_sel}")
    print(f"Test 3 - Log in Team A and select Case 2: {'PASS' if results[3][0] else 'FAIL'}")

    # 4. Confirm Team A's selected case is saved
    code, prog_res_a = req(f"/api/teams/progress?team_id={team_a_id}", "GET")
    prog_a = prog_res_a.get("progress", {}) if isinstance(prog_res_a, dict) else {}
    results[4] = (code == 200 and prog_a.get("caseId") == "case-02" and prog_a.get("logicalState") in ("CASE_SELECTED", "ROUND_1_IN_PROGRESS"), f"Progress: {prog_a}")
    print(f"Test 4 - Confirm Team A's selected case saved: {'PASS' if results[4][0] else 'FAIL'} (Case: {prog_a.get('caseId')}, State: {prog_a.get('logicalState')})")

    # 5. Log in as Team B and confirm it can independently select Case 2 if shared cases are allowed
    code, login_b = req("/api/teams/login", "POST", {"teamId": team_b_id, "pin": "2222"})
    token_b = login_b.get("token")
    code_sel_b, res_sel_b = req("/api/teams/select-case", "POST", {"teamId": team_b_id, "caseId": "case-02"}, {"Authorization": f"Bearer {token_b}"})
    code_prog_b, prog_res_b = req(f"/api/teams/progress?team_id={team_b_id}", "GET")
    prog_b = prog_res_b.get("progress", {}) if isinstance(prog_res_b, dict) else {}
    results[5] = (code == 200 and code_sel_b == 200 and prog_b.get("caseId") == "case-02", f"Select B: {code_sel_b}, Case: {prog_b.get('caseId')}")
    print(f"Test 5 - Team B independently selects Case 2: {'PASS' if results[5][0] else 'FAIL'}")

    # 6. Confirm Team B does not inherit Team A's round status
    results[6] = (prog_b.get("round1", {}).get("completed") is False and prog_b.get("round2", {}).get("completed") is False and prog_b.get("logicalState") in ("CASE_SELECTED", "ROUND_1_IN_PROGRESS"), f"State: {prog_b.get('logicalState')}")
    print(f"Test 6 - Team B does not inherit round status: {'PASS' if results[6][0] else 'FAIL'} (Round 1 Completed: {prog_b.get('round1', {}).get('completed')})")

    # 7. Complete Round 1 for Team A
    # Start timer for Round 1 Team A
    req(f"/api/round/timer?round=1&team_id={team_a_id}&case_id=case-02", "GET")
    # Early submit Round 1 answers for Team A (Case 2 R1 keys: 1:C=2, 2:B=1, 3:A=0, 4:D=3, 5:C=2)
    sample_answers_a1 = {0: 2, 1: 1, 2: 0, 3: 3, 4: 2}
    req("/api/round/submit-early", "POST", {
        "round": 1,
        "teamId": team_a_id,
        "caseId": "case-02",
        "answers": sample_answers_a1
    })
    # Also auto-submit Round 1 for Team A to seal completion
    code_auto_a1, res_auto_a1 = req("/api/round/auto-submit", "POST", {
        "round": 1,
        "teamId": team_a_id,
        "caseId": "case-02",
        "answers": sample_answers_a1
    })
    code_prog_a_after, prog_res_a_after = req(f"/api/teams/progress?team_id={team_a_id}", "GET")
    prog_a_after = prog_res_a_after.get("progress", {}) if isinstance(prog_res_a_after, dict) else {}
    results[7] = (code_auto_a1 == 200 and prog_a_after.get("round1", {}).get("completed") is True and prog_a_after.get("logicalState") in ("ROUND_1_COMPLETED", "ROUND_2_IN_PROGRESS"), f"Round 1 completed: {prog_a_after.get('round1')}")
    print(f"Test 7 - Complete Round 1 for Team A: {'PASS' if results[7][0] else 'FAIL'} (State: {prog_a_after.get('logicalState')})")

    # 8. Log in as a newly registered Team C
    team_c_id = f"TX-REG-C-{ts}"
    req("/api/teams/register", "POST", {
        "teamId": team_c_id,
        "teamName": "Team Charlie Recon",
        "collegeName": "Tech Institute",
        "department": "Cybersecurity",
        "teamSize": 1,
        "members": [{"name": "Charlie", "email": "c@recon.edu", "phone": "9998887773"}],
        "pinRaw": "3333"
    })
    code_login_c, login_c = req("/api/teams/login", "POST", {"teamId": team_c_id, "pin": "3333"})
    results[8] = (code_login_c == 200 and login_c.get("success") is True, f"Login C code: {code_login_c}")
    print(f"Test 8 - Register and log in newly registered Team C: {'PASS' if results[8][0] else 'FAIL'}")

    # 9. Confirm Team C starts at its own case-selection stage
    prog_c = login_c.get("progress", {})
    results[9] = (prog_c.get("logicalState") == "CASE_NOT_SELECTED" and prog_c.get("caseId") is None, f"State: {prog_c.get('logicalState')}, Case: {prog_c.get('caseId')}")
    print(f"Test 9 - Team C starts at CASE_NOT_SELECTED: {'PASS' if results[9][0] else 'FAIL'}")

    # 10. Confirm Team C is not sent directly to Round 2
    results[10] = (prog_c.get("round1", {}).get("completed") is False and prog_c.get("round2", {}).get("completed") is False and prog_c.get("logicalState") != "ROUND_2_IN_PROGRESS", f"Round 1 completed: {prog_c.get('round1')}")
    print(f"Test 10 - Team C is NOT sent directly to Round 2: {'PASS' if results[10][0] else 'FAIL'}")

    # 11. Log out and log back in as Team A
    code_login_a2, login_a2 = req("/api/teams/login", "POST", {"teamId": team_a_id, "pin": "1111"})
    prog_a2 = login_a2.get("progress", {})
    results[11] = (code_login_a2 == 200 and login_a2.get("success") is True, f"Re-login code: {code_login_a2}")
    print(f"Test 11 - Log out and log back in as Team A: {'PASS' if results[11][0] else 'FAIL'}")

    # 12. Confirm Team A's correct progress is restored
    results[12] = (prog_a2.get("caseId") == "case-02" and prog_a2.get("round1", {}).get("completed") is True and prog_a2.get("logicalState") == "ROUND_1_COMPLETED", f"Restored progress: {prog_a2}")
    print(f"Test 12 - Team A's correct progress is restored: {'PASS' if results[12][0] else 'FAIL'} (Case: {prog_a2.get('caseId')}, Round 1 Completed: {prog_a2.get('round1', {}).get('completed')})")

    # 13. Refresh the page during a round and verify its timer is not reset
    # Start timer for Team B Round 1
    code_tb1, t_b1 = req(f"/api/round/timer?round=1&team_id={team_b_id}&case_id=case-02", "GET")
    time.sleep(1.2)
    # Simulate page refresh by querying timer again
    code_tb2, t_b2 = req(f"/api/round/timer?round=1&team_id={team_b_id}&case_id=case-02", "GET")
    end1 = t_b1.get("endTime")
    end2 = t_b2.get("endTime")
    rem1 = t_b1.get("remainingSeconds")
    rem2 = t_b2.get("remainingSeconds")
    timer_consistent = (end1 == end2 and rem2 < rem1)
    results[13] = (timer_consistent, f"end1={end1}, end2={end2}, rem1={rem1}, rem2={rem2}")
    print(f"Test 13 - Page refresh does NOT restart round timer: {'PASS' if results[13][0] else 'FAIL'} (EndTime constant, rem: {rem1}s -> {rem2}s)")

    # Authenticate Admin for admin tests
    code_admin_login, admin_login = req("/api/admin/login", "POST", {
        "adminId": "admin_cse",
        "password": "traceX@2026"
    })
    admin_token = admin_login.get("token")

    # 14. Verify that submissions and scores are associated with the correct team
    # Submit Round 2 for Team A (Case 2 R2 keys: 1:B=1, 2:A=0, 3:D=3, 4:C=2, 5:B=1)
    sample_answers_a2 = {0: 1, 1: 0, 2: 3, 3: 2, 4: 1}
    req("/api/round/auto-submit", "POST", {
        "round": 2,
        "teamId": team_a_id,
        "caseId": "case-02",
        "answers": sample_answers_a2
    })
    code_evals, evals_data = req("/api/admin/evaluations", "GET", headers={"Authorization": f"Bearer {admin_token}"})
    eval_list = evals_data.get("evaluations", []) if isinstance(evals_data, dict) else []
    team_a_eval = next((e for e in eval_list if e.get("teamId") == team_a_id), None)
    team_b_eval = next((e for e in eval_list if e.get("teamId") == team_b_id), None)
    score_a = team_a_eval.get("totalScore") if team_a_eval else 0
    score_b = team_b_eval.get("totalScore") if team_b_eval else 0
    results[14] = (team_a_eval is not None and score_a > 0 and score_a != score_b, f"Score A: {score_a}, Score B: {score_b}")
    print(f"Test 14 - Submissions and scores associated with correct team: {'PASS' if results[14][0] else 'FAIL'} (Team A Score: {score_a}, Team B Score: {score_b})")

    # 15. Confirm the original registration, evaluation, and result-publication workflows still work
    code_pub, res_pub = req("/api/admin/event-control", "POST", {"action": "publish_results"}, headers={"Authorization": f"Bearer {admin_token}"})
    code_res_a, res_a = req(f"/api/participant/result?team_id={team_a_id}", "GET")
    results[15] = (code_pub == 200 and res_pub.get("resultsPublished") is True and code_res_a == 200 and res_a.get("isPublished") is True, f"Publish: {res_pub}, Result: {res_a}")
    print(f"Test 15 - Registration, evaluation, and result-publication workflows work: {'PASS' if results[15][0] else 'FAIL'}")

    # 16. Log in as an authorized administrator
    results[16] = (code_admin_login == 200 and admin_token is not None, f"Admin token: {bool(admin_token)}")
    print(f"Test 16 - Log in as authorized administrator: {'PASS' if results[16][0] else 'FAIL'}")

    # 17. Confirm TEAM MANAGEMENT displays registered teams
    code_teams, teams_data = req("/api/admin/teams", "GET", headers={"Authorization": f"Bearer {admin_token}"})
    teams_list = teams_data.get("teams", []) if isinstance(teams_data, dict) else []
    found_a = any(t.get("teamId") == team_a_id for t in teams_list)
    results[17] = (code_teams == 200 and len(teams_list) > 0 and found_a, f"Teams loaded: {len(teams_list)}, Team A found: {found_a}")
    print(f"Test 17 - TEAM MANAGEMENT displays registered teams: {'PASS' if results[17][0] else 'FAIL'} ({len(teams_list)} teams)")

    # 18. Search for a specific Team ID
    matched = [t for t in teams_list if t.get("teamId") == team_a_id]
    results[18] = (len(matched) == 1 and matched[0].get("teamName") == "Team Alpha Cyber", f"Matched: {matched}")
    print(f"Test 18 - Search for specific Team ID ({team_a_id}): {'PASS' if results[18][0] else 'FAIL'}")

    # 19. Delete or deactivate a team that has not participated (Team C has no case progress, answers, or timers)
    code_del_c, res_del_c = req("/api/admin/teams/delete", "POST", {
        "teamId": team_c_id,
        "reason": "Test deletion for non-participated team"
    }, headers={"Authorization": f"Bearer {admin_token}"})
    results[19] = (code_del_c == 200 and res_del_c.get("success") is True, f"Delete code: {code_del_c}, res: {res_del_c}")
    print(f"Test 19 - Delete/deactivate unparticipated team ({team_c_id}): {'PASS' if results[19][0] else 'FAIL'} (Action: {res_del_c.get('action')})")

    # 20. Confirm the intended team is removed from the active team list
    code_teams_after, teams_data_after = req("/api/admin/teams", "GET", headers={"Authorization": f"Bearer {admin_token}"})
    teams_after = teams_data_after.get("teams", []) if isinstance(teams_data_after, dict) else []
    found_c_active = any(t.get("teamId") == team_c_id and t.get("status") in ("Registered", "Active") for t in teams_after)
    results[20] = (not found_c_active, f"Team C found in active list: {found_c_active}")
    print(f"Test 20 - Unparticipated team removed from active registry: {'PASS' if results[20][0] else 'FAIL'}")

    # 21. Confirm that the deleted/deactivated team cannot log in
    code_login_c_after, res_login_c_after = req("/api/teams/login", "POST", {"teamId": team_c_id, "pin": "3333"})
    results[21] = (code_login_c_after in (401, 403, 404), f"Login code after deletion: {code_login_c_after}")
    print(f"Test 21 - Deleted/deactivated team cannot log in: {'PASS' if results[21][0] else 'FAIL'} (Response: {code_login_c_after})")

    # 22. Confirm another team's account and progress remain unchanged
    code_check_a, prog_res_check_a = req(f"/api/teams/progress?team_id={team_a_id}", "GET")
    prog_check_a = prog_res_check_a.get("progress", {}) if isinstance(prog_res_check_a, dict) else {}
    results[22] = (code_check_a == 200 and prog_check_a.get("caseId") == "case-02" and prog_check_a.get("round1", {}).get("completed") is True, f"Prog A: {prog_check_a}")
    print(f"Test 22 - Other team's account and progress untouched: {'PASS' if results[22][0] else 'FAIL'}")

    # 23. Attempt deletion without admin authorization and confirm the server rejects it
    code_unauth, res_unauth = req("/api/admin/teams/delete", "POST", {
        "teamId": team_b_id,
        "reason": "Unauthorized attempt"
    }) # No admin token
    results[23] = (code_unauth in (401, 403), f"Unauth code: {code_unauth}")
    print(f"Test 23 - Deletion without admin authorization rejected: {'PASS' if results[23][0] else 'FAIL'} (Code: {code_unauth})")

    # 24. Attempt to delete a nonexistent Team ID and confirm an appropriate error
    code_fake, res_fake = req("/api/admin/teams/delete", "POST", {
        "teamId": "TX-NONEXISTENT-9999",
        "reason": "Delete non-existent"
    }, headers={"Authorization": f"Bearer {admin_token}"})
    results[24] = (code_fake == 404, f"Fake delete code: {code_fake}")
    print(f"Test 24 - Delete nonexistent Team ID returns 404: {'PASS' if results[24][0] else 'FAIL'} (Code: {code_fake})")

    # 25. Confirm historical scores and published results are preserved according to retention rules (Deactivate Team A which has participated)
    code_del_a, res_del_a = req("/api/admin/teams/delete", "POST", {
        "teamId": team_a_id,
        "reason": "Deactivate participated team"
    }, headers={"Authorization": f"Bearer {admin_token}"})
    # Since Team A has submissions/scores, retention rule requires soft-deactivation (DEACTIVATED)
    code_evals_a_after, evals_a_data = req("/api/admin/evaluations", "GET", headers={"Authorization": f"Bearer {admin_token}"})
    evals_list_after = evals_a_data.get("evaluations", []) if isinstance(evals_a_data, dict) else []
    eval_a_after = next((e for e in evals_list_after if e.get("teamId") == team_a_id), None)
    score_preserved = eval_a_after is not None and eval_a_after.get("totalScore") is not None
    code_login_a_after, res_login_a_after = req("/api/teams/login", "POST", {"teamId": team_a_id, "pin": "1111"})
    # Login must now be barred (403)
    results[25] = (res_del_a.get("action") == "DEACTIVATED" and score_preserved and code_login_a_after == 403, f"Action: {res_del_a.get('action')}, Score Preserved: {score_preserved}, Login barred: {code_login_a_after}")
    print(f"Test 25 - Participated team soft-deactivated; historical data preserved, login barred (403): {'PASS' if results[25][0] else 'FAIL'}")

    # 26. Confirm the deletion or deactivation audit record is created
    code_audit, audit_data = req("/api/admin/audit-logs", "GET", headers={"Authorization": f"Bearer {admin_token}"})
    audit_logs = audit_data.get("auditLogs", []) if isinstance(audit_data, dict) else []
    found_audit = False
    for log in audit_logs:
        if team_a_id in str(log) or team_c_id in str(log):
            found_audit = True
            break
    results[26] = (code_audit == 200 and found_audit, f"Audit logs: {len(audit_logs)}, found: {found_audit}")
    print(f"Test 26 - Audit log entry created for team deletion/deactivation: {'PASS' if results[26][0] else 'FAIL'}")

    print("=" * 70)
    all_passed = all(r[0] for r in results.values())
    total_passed = sum(1 for r in results.values() if r[0])
    print(f"REGRESSION SUITE COMPLETED: {total_passed}/26 TESTS PASSED. OVERALL: {'SUCCESS' if all_passed else 'FAILURE'}")
    print("=" * 70)

    if not all_passed:
        print("Failed tests details:")
        for t_idx, (passed, info) in results.items():
            if not passed:
                print(f"  Test {t_idx} FAILED: {info}")

    return all_passed

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
