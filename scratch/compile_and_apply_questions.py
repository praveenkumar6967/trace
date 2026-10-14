# scratch/compile_and_apply_questions.py
import json
import sqlite3
import os
import sys
import time

# Import the 3 batches
from case_data_batch1 import BATCH_1
from case_data_batch2 import BATCH_2
from case_data_batch3 import BATCH_3

def main():
    print("[1/5] Merging all 15 cases...")
    all_cases = {}
    all_cases.update(BATCH_1)
    all_cases.update(BATCH_2)
    all_cases.update(BATCH_3)

    print(f"Total cases assembled: {len(all_cases)}")
    assert len(all_cases) == 15, f"Expected 15 cases, got {len(all_cases)}"

    print("\n[2/5] Validating question content and answer keys...")
    total_q_count = 0
    option_letters = ['A', 'B', 'C', 'D']

    for cid in sorted(all_cases.keys()):
        case = all_cases[cid]
        r1_qs = case.get('questions', [])
        r2_qs = case.get('round2Questions', [])

        assert len(r1_qs) == 15, f"Case {cid} Round 1 has {len(r1_qs)} questions (must be 15)"
        assert len(r2_qs) == 15, f"Case {cid} Round 2 has {len(r2_qs)} questions (must be 15)"

        # Check Round 1 questions
        seen_r1 = set()
        for idx, q in enumerate(r1_qs):
            txt = q['text'].strip()
            assert txt, f"Case {cid} R1 Q{idx+1} has empty text"
            assert txt.lower() not in seen_r1, f"Duplicate question in Case {cid} R1: '{txt}'"
            seen_r1.add(txt.lower())

            opts = q.get('options', [])
            assert len(opts) == 4, f"Case {cid} R1 Q{idx+1} must have 4 options, found {len(opts)}"
            for opt_idx, opt in enumerate(opts):
                assert opt.strip(), f"Case {cid} R1 Q{idx+1} option {opt_idx} is empty"
            assert len(set(opts)) == 4, f"Case {cid} R1 Q{idx+1} has duplicate options: {opts}"

            ans = q.get('answer')
            assert ans in (0, 1, 2, 3), f"Case {cid} R1 Q{idx+1} invalid answer {ans}"
            assert q.get('explanation', '').strip(), f"Case {cid} R1 Q{idx+1} missing explanation"

        # Check Round 2 questions
        seen_r2 = set()
        for idx, q in enumerate(r2_qs):
            txt = q['text'].strip()
            assert txt, f"Case {cid} R2 Q{idx+1} has empty text"
            assert txt.lower() not in seen_r2, f"Duplicate question in Case {cid} R2: '{txt}'"
            seen_r2.add(txt.lower())

            opts = q.get('options', [])
            assert len(opts) == 4, f"Case {cid} R2 Q{idx+1} must have 4 options, found {len(opts)}"
            for opt_idx, opt in enumerate(opts):
                assert opt.strip(), f"Case {cid} R2 Q{idx+1} option {opt_idx} is empty"
            assert len(set(opts)) == 4, f"Case {cid} R2 Q{idx+1} has duplicate options: {opts}"

            ans = q.get('answer')
            assert ans in (0, 1, 2, 3), f"Case {cid} R2 Q{idx+1} invalid answer {ans}"
            assert q.get('explanation', '').strip(), f"Case {cid} R2 Q{idx+1} missing explanation"

        total_q_count += len(r1_qs) + len(r2_qs)
        print(f"  [OK] {cid}: {case['name']} (15 R1 + 15 R2 = 30 questions verified)")

    print(f"\nAll {total_q_count} questions successfully validated (100% strict compliance).")
    assert total_q_count == 450, f"Expected 450 questions total, got {total_q_count}"

    # Write cases_seed.json
    print("\n[3/5] Writing backend authoritative cases_seed.json...")
    seed_path = os.path.join(os.path.dirname(__file__), '..', 'cases_seed.json')
    seed_path = os.path.abspath(seed_path)
    with open(seed_path, 'w', encoding='utf-8') as f:
        json.dump(all_cases, f, indent=2, ensure_ascii=False)
    print(f"  [OK] Saved {seed_path} ({os.path.getsize(seed_path)} bytes)")

    # Update SQLite Database
    print("\n[4/5] Updating SQLite database tracex.db...")
    db_path = os.path.join(os.path.dirname(__file__), '..', 'tracex.db')
    db_path = os.path.abspath(db_path)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    now_iso = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())

    # Update Cases table
    for idx, (cid, case) in enumerate(all_cases.items()):
        ev_json = json.dumps(case.get('evidence', []), ensure_ascii=False)
        r2_ev_json = json.dumps(case.get('round2Evidence', []), ensure_ascii=False)
        c.execute('''
            UPDATE cases
            SET name = ?, summary = ?, evidence_json = ?, round2_evidence_json = ?, updated_at = ?, updated_by = 'UPDATE_QUESTIONS_DIRECTIVE'
            WHERE case_id = ?
        ''', (case['name'], case['summary'], ev_json, r2_ev_json, now_iso, cid))

    # Clear and repopulate questions table cleanly
    c.execute("DELETE FROM questions")

    questions_inserted = 0
    for cid, case in all_cases.items():
        evidence_list = case.get('evidence', [])
        r2_evidence_list = case.get('round2Evidence', [])

        # Round 1
        for q_idx, q in enumerate(case.get('questions', [])):
            qid = f"{cid}-r1-q{q_idx+1:02d}"
            opts = q['options']
            ans_letter = option_letters[q['answer']]
            ev_ref = evidence_list[q_idx % len(evidence_list)]['title'] if evidence_list else ''
            expl = q.get('explanation', '')

            c.execute('''
                INSERT INTO questions (
                    id, case_id, round, order_num, question_text,
                    option_a, option_b, option_c, option_d,
                    correct_answer, marks, evidence_ref,
                    created_at, updated_at, updated_by
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                qid, cid, 1, q_idx + 1, q['text'],
                opts[0], opts[1], opts[2], opts[3],
                ans_letter, 1, ev_ref,
                now_iso, now_iso, 'UPDATE_QUESTIONS_DIRECTIVE'
            ))
            questions_inserted += 1

        # Round 2
        for q_idx, q in enumerate(case.get('round2Questions', [])):
            qid = f"{cid}-r2-q{q_idx+1:02d}"
            opts = q['options']
            ans_letter = option_letters[q['answer']]
            ev_ref = r2_evidence_list[q_idx % len(r2_evidence_list)]['title'] if r2_evidence_list else ''
            expl = q.get('explanation', '')

            c.execute('''
                INSERT INTO questions (
                    id, case_id, round, order_num, question_text,
                    option_a, option_b, option_c, option_d,
                    correct_answer, marks, evidence_ref,
                    created_at, updated_at, updated_by
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                qid, cid, 2, q_idx + 1, q['text'],
                opts[0], opts[1], opts[2], opts[3],
                ans_letter, 1, ev_ref,
                now_iso, now_iso, 'UPDATE_QUESTIONS_DIRECTIVE'
            ))
            questions_inserted += 1

    conn.commit()
    conn.close()
    print(f"  [OK] Replaced SQLite questions table with {questions_inserted} authoritative records.")

    # Update assets/js/investigation-data.js (STRIPPED of all answer keys for candidate privacy)
    print("\n[5/5] Generating client-side investigation-data.js (Strict Answer Privacy)...")
    inv_data_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'js', 'investigation-data.js')
    inv_data_path = os.path.abspath(inv_data_path)

    # Build sanitized client dictionary
    client_cases = {}
    for cid, case in all_cases.items():
        client_cases[cid] = {
            "id": case["id"],
            "name": case["name"],
            "summary": case["summary"],
            "evidence": case.get("evidence", []),
            "round2Evidence": case.get("round2Evidence", []),
            "questions": [
                {
                    "text": q["text"],
                    "options": q["options"]
                    # STRICT PRIVACY: zero answer, zero explanation
                }
                for q in case.get("questions", [])
            ],
            "round2Questions": [
                {
                    "text": q["text"],
                    "options": q["options"]
                    # STRICT PRIVACY: zero answer, zero explanation
                }
                for q in case.get("round2Questions", [])
            ]
        }

    js_header = """/**
 * TRACE × X — CYBER CRIME INVESTIGATION
 * ROUND 1 & ROUND 2 INVESTIGATION DATASET: 15 CASES
 * Evidence Dossiers & Exactly 15 Questions per Round (30 Questions Total per Case)
 * T.J.S. ENGINEERING COLLEGE | DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING
 *
 * NOTE: STRICT CANDIDATE PRIVACY ENFORCED.
 * Authoritative answer keys and evaluation metrics reside exclusively in the backend SQLite database.
 */

'use strict';

const TRACE_INVESTIGATION_CASES = """

    js_footer = """;

// Expose on window for client-side rendering
if (typeof window !== 'undefined') {
  window.TRACE_INVESTIGATION_CASES = TRACE_INVESTIGATION_CASES;
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { TRACE_INVESTIGATION_CASES };
}
"""

    with open(inv_data_path, 'w', encoding='utf-8') as f:
        f.write(js_header)
        json.dump(client_cases, f, indent=2, ensure_ascii=False)
        f.write(js_footer)

    print(f"  [OK] Saved client dataset: {inv_data_path} ({os.path.getsize(inv_data_path)} bytes)")

    # Verify that '"answer":' is NOT present in investigation-data.js
    with open(inv_data_path, 'r', encoding='utf-8') as f:
        inv_code = f.read()
    assert '"answer":' not in inv_code, "Security check failed: '\"answer\":' found in investigation-data.js!"
    assert '"correct_answer":' not in inv_code, "Security check failed: '\"correct_answer\":' found in investigation-data.js!"
    print("  [OK] Security assertion passed: Zero answer keys exposed in client file.")

    print("\n=======================================================")
    print(f"COMPILATION COMPLETE: All {questions_inserted} questions updated across all 15 cases!")
    print("=======================================================")

if __name__ == '__main__':
    main()
