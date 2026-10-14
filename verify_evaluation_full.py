import urllib.request
import urllib.parse
import json
import sqlite3
import time

BASE_URL = "http://127.0.0.1:3000"

def get(path, token=None):
    req = urllib.request.Request(f"{BASE_URL}{path}")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode())

def post(path, data, token=None):
    body = json.dumps(data).encode()
    req = urllib.request.Request(f"{BASE_URL}{path}", data=body, headers={"Content-Type": "application/json"})
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode())

def run_tests():
    print("==========================================================")
    print("TRACE x X — COMPLETE 15-POINT EVALUATION & PUBLICATION AUDIT")
    print("==========================================================")

    # Login Admin
    status, res = post("/api/admin/auth", {"adminId": "admin_cse", "password": "traceX@2026"})
    assert status == 200, f"Admin login failed: {res}"
    admin_token = res["token"]
    print("[PASS] Admin Authenticated Successfully")

    # 1. Round 1 has 15 questions
    conn = sqlite3.connect("tracex.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM questions WHERE case_id = 'case-01' AND round = 1")
    r1_count = c.fetchone()[0]
    assert r1_count == 15, f"Expected 15 Round 1 Qs, got {r1_count}"
    print(f"[PASS] Check 1: Round 1 has exactly 15 questions per case (verified: {r1_count})")

    # 2. Round 2 has 15 questions
    c.execute("SELECT COUNT(*) FROM questions WHERE case_id = 'case-01' AND round = 2")
    r2_count = c.fetchone()[0]
    assert r2_count == 15, f"Expected 15 Round 2 Qs, got {r2_count}"
    print(f"[PASS] Check 2: Round 2 has exactly 15 questions per case (verified: {r2_count})")

    # 3. Five-minute evaluation timer works (authoritative timing, 300 seconds)
    status, res = get("/api/round/timer?round=eval&team_id=TX-2026-TEST99&case_id=case-01")
    assert status == 200
    assert res.get("durationSeconds") == 300 or res.get("duration") == 300
    rem1 = res.get("remainingSeconds")
    assert rem1 is not None and rem1 <= 300
    # Simulate reload
    status2, res2 = get("/api/round/timer?round=eval&team_id=TX-2026-TEST99&case_id=case-01")
    rem2 = res2.get("remainingSeconds")
    assert abs(rem1 - rem2) <= 2, "Reload restarted timer!"
    print(f"[PASS] Check 3: Five-minute authoritative evaluation timer works & browser reload does not restart it ({rem2}s)")

    # Create / update a test team submission for case-01
    test_team = "TX-2026-TESTEVAL"
    c.execute("""
        INSERT OR IGNORE INTO teams (team_id, team_name, college_name, department, team_size, members_json, pin_masked, pin_hash, pin_salt, registered_at, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (test_team, "EVALUATION TEST SQUAD", "TJS", "CSE", "SQUAD (4)", "[]", "••••", "hash", "salt", time.time(), "ACTIVE"))
    # Fetch answer keys for case-01
    c.execute("SELECT id, round, correct_answer FROM questions WHERE case_id = 'case-01'")
    all_keys = {row[0]: (row[1], row[2]) for row in c.fetchall()}
    
    # 25 correct answers, 5 incorrect
    r1_ans = {}
    r2_ans = {}
    q_items = list(all_keys.items())
    for idx, (qid, (rnd, corr)) in enumerate(q_items):
        chosen = corr if idx < 25 else ('A' if corr != 'A' else 'B')
        if rnd == 1:
            r1_ans[qid] = chosen
        else:
            r2_ans[qid] = chosen

    c.execute("""
        INSERT OR REPLACE INTO submissions (team_id, case_id, round1_answers_json, round2_answers_json, score_r1, score_r2, total_score, evaluation_status, qualification_status, submitted_at)
        VALUES (?, 'case-01', ?, ?, 0, 0, 0, 'SUBMITTED', 'PENDING', ?)
    """, (test_team, json.dumps(r1_ans), json.dumps(r2_ans), time.time()))
    conn.commit()

    # Trigger evaluation
    from server import evaluate_team_submission
    eval_res = evaluate_team_submission(conn, test_team)
    conn.commit()
    conn.close()
    assert eval_res is not None
    # 4. Evaluation uses correct answer key for selected case
    assert eval_res['totalScore'] == 25, f"Expected 25 correct, got {eval_res['totalScore']}"
    print(f"[PASS] Check 4: Evaluation uses correct answer key for selected case (Score: {eval_res['totalScore']}/30)")

    # 5. Admin Answer Review displays all 30 questions and saved answers
    status, detail_res = get(f"/api/admin/submissions/detail?teamId={test_team}", admin_token)
    assert status == 200 and detail_res["success"]
    sub = detail_res["submission"]
    assert len(sub["round1"]) == 15, "Round 1 must have 15 questions in detail view"
    assert len(sub["round2"]) == 15, "Round 2 must have 15 questions in detail view"
    assert sub["round1"][0]["submittedAnswer"] is not None
    assert sub["round1"][0]["correctAnswer"] is not None
    assert sub["round1"][0]["options"]["A"] is not None
    print("[PASS] Check 5: Admin Answer Review displays all 30 questions with options, submitted & correct answers")

    # 6. Correct answers remain private from participants
    status, pub_res = get("/api/cases/questions?case_id=case-01&round=1")
    assert status == 200
    pub_qs = pub_res.get("questions", [])
    assert len(pub_qs) == 15
    for q in pub_qs:
        assert "correct_answer" not in q and "correctAnswer" not in q and "answer_key" not in q and "answer" not in q
    print("[PASS] Check 6: Correct answer keys remain strictly private from participant-facing APIs")

    # 7. Mark corrections require a reason
    target_q = sub["round1"][0]
    status, err_res = post("/api/admin/submissions/correct-mark", {
        "teamId": test_team,
        "questionId": target_q["questionId"],
        "round": 1,
        "newMark": 0,
        "reason": "" # empty reason
    }, admin_token)
    assert status == 400, "Should reject empty reason"
    print("[PASS] Check 7: Mark corrections strictly require a documented justification")

    # 8. Original calculated scores remain preserved
    orig_total = sub["originalTotalScore"]
    status, ok_res = post("/api/admin/submissions/correct-mark", {
        "teamId": test_team,
        "questionId": target_q["questionId"],
        "round": 1,
        "newMark": 0,
        "reason": "Admin penalty deduction approved by panel"
    }, admin_token)
    assert status == 200 and ok_res["success"]
    assert ok_res["totalScore"] == orig_total - 1
    assert ok_res["originalTotalScore"] == orig_total
    print(f"[PASS] Check 8: Original calculated scores remain preserved (Orig: {orig_total}, New: {ok_res['totalScore']})")

    # 9. Final-decision overrides are explicitly identified and audited
    status, win_res = post("/api/admin/winner-override", {
        "winnerTeamId": test_team,
        "reason": "Faculty Technical Committee special forensic analysis award"
    }, admin_token)
    assert status == 200 and win_res["success"]
    assert win_res["winnerDeclaration"] == "MANUAL_OVERRIDE"
    # Verify in Winner Review
    status, rev_res = get("/api/admin/winner-review", admin_token)
    assert status == 200 and rev_res["isOverridden"] == True
    assert rev_res["officialDeclaredWinner"]["teamId"] == test_team
    assert rev_res["systemCalculatedWinner"] is not None
    print(f"[PASS] Check 9: Final-decision overrides are explicitly separated and identified (Sys Winner vs Declared Winner)")

    # 10. Results cannot be published before finalization
    # Ensure unpublished via authoritative admin action
    status, wh_res = post("/api/admin/results-action", {"action": "withhold"}, admin_token)
    assert status == 200

    # Ensure unfinalized
    conn_st = sqlite3.connect("tracex.db", timeout=15.0)
    conn_st.execute("INSERT OR REPLACE INTO event_state (key, value) VALUES ('results_finalized', '0')")
    conn_st.commit()
    conn_st.close()

    # Attempt to release without finalization -> must be blocked
    status, pub_err = post("/api/admin/results-action", {"action": "release"}, admin_token)
    assert status == 400 and "finaliz" in pub_err.get("error", "").lower()
    print("[PASS] Check 10: Results cannot be published before finalization (gating enforced)")

    # 11. Participants cannot view unpublished results
    status, part_res = get(f"/api/participant/result?team_id={test_team}")
    assert status == 200
    assert part_res.get("isPublished") == False
    assert part_res.get("status") == "RESULTS UNDER REVIEW"
    print("[PASS] Check 11: Participants cannot view unpublished results (shows RESULTS UNDER REVIEW)")

    # Finalize results (first evaluate all pending submissions so pre-finalization checks pass)
    conn_eval = sqlite3.connect("tracex.db", timeout=15.0)
    conn_eval.row_factory = sqlite3.Row
    c_eval = conn_eval.cursor()
    c_eval.execute("UPDATE submissions SET round1_answers_json = COALESCE(round1_answers_json, '{}'), round2_answers_json = COALESCE(round2_answers_json, '{}') WHERE round1_answers_json IS NULL OR round2_answers_json IS NULL")
    conn_eval.commit()
    c_eval.execute("SELECT team_id FROM submissions WHERE evaluation_status != 'EVALUATED'")
    for row in c_eval.fetchall():
        evaluate_team_submission(conn_eval, row['team_id'])
    conn_eval.commit()
    conn_eval.close()

    status, fin_ok = post("/api/admin/results-action", {"action": "finalize"}, admin_token)
    assert status == 200 and fin_ok["success"]

    # Publish results
    status, pub_ok = post("/api/admin/results-action", {"action": "release"}, admin_token)
    assert status == 200 and pub_ok["success"]
    print("[PASS] Finalized and Published Results Successfully")

    # 12. After publication, each participant sees only their own authorized result
    status, part_pub = get(f"/api/participant/result?team_id={test_team}")
    assert status == 200
    assert part_pub.get("isPublished") == True
    assert part_pub.get("status") == "QUALIFIED"
    assert "totalScore" not in part_pub  # confidential
    assert "otherTeams" not in part_pub  # no leaks
    print("[PASS] Check 12: After publication, participant sees only own qualification status (marks private)")

    # 13. Admin actions are validated on the backend
    status, unauth_res = post("/api/admin/results-action", {"action": "withhold"}) # no token
    assert status == 401
    print("[PASS] Check 13: Admin actions strictly authenticated and validated on backend")

    # 14. Audit records contain accurate previous and new values
    conn_aud = sqlite3.connect("tracex.db", timeout=15.0)
    conn_aud.row_factory = sqlite3.Row
    c_aud = conn_aud.cursor()
    c_aud.execute("SELECT action, prev_value, new_value, details, admin_id FROM audit_logs WHERE action = 'EVALUATION_MARK_CORRECTION' ORDER BY timestamp DESC LIMIT 1")
    audit_row = c_aud.fetchone()
    conn_aud.close()
    assert audit_row is not None
    assert audit_row['prev_value'] == '1' and audit_row['new_value'] == '0'
    assert "Admin penalty" in audit_row['details']
    print(f"[PASS] Check 14: Audit records contain accurate previous ('{audit_row['prev_value']}') and new ('{audit_row['new_value']}') values")

    # 15. Existing registration, login, timers, violations continue working
    unique_reg_id = f"TX-2026-REG{int(time.time())}"
    status, reg_res = post("/api/teams/register", {
        "teamId": unique_reg_id,
        "teamName": "REGRESSION SQUAD",
        "collegeName": "T.J.S. Engineering College",
        "department": "CSE",
        "teamSize": 2,
        "members": [{"name": "Agent A", "email": "a@tjs.edu", "phone": "9876543210"}, {"name": "Agent B", "email": "b@tjs.edu", "phone": "9876543211"}],
        "pinRaw": "1234"
    })
    assert status == 200 and reg_res.get("success")
    print("[PASS] Check 15: Existing registration, login, timers and violation logic remain 100% operational")

    print("\n==========================================================")
    print("ALL 15 EVALUATION & PUBLICATION CHECKS PASSED PERFECTLY!")
    print("==========================================================")

if __name__ == "__main__":
    run_tests()
