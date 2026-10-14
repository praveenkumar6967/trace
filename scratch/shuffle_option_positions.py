# scratch/shuffle_option_positions.py
import json
import sqlite3
import os
import random

# Seed for reproducible, balanced distribution
random.seed(20261013)

with open('cases_seed.json', 'r', encoding='utf-8') as f:
    cases = json.load(f)

option_letters = ['A', 'B', 'C', 'D']

total_shuffled = 0
letter_counts = {'A': 0, 'B': 0, 'C': 0, 'D': 0}

for cid_idx, (cid, case) in enumerate(cases.items()):
    for r_key, r_num in [('questions', 1), ('round2Questions', 2)]:
        qs = case.get(r_key, [])
        for q_idx, q in enumerate(qs):
            old_opts = list(q['options'])
            old_ans = q['answer']
            correct_val = old_opts[old_ans]

            # Deterministic, balanced target index: cycle through 0, 1, 2, 3 with pseudo-random offset
            target_idx = (cid_idx * 7 + r_num * 11 + q_idx * 3) % 4

            # Create new options list with correct answer at target_idx
            remaining_opts = [opt for i, opt in enumerate(old_opts) if i != old_ans]
            random.shuffle(remaining_opts)

            new_opts = [None] * 4
            new_opts[target_idx] = correct_val
            rem_i = 0
            for i in range(4):
                if new_opts[i] is None:
                    new_opts[i] = remaining_opts[rem_i]
                    rem_i += 1

            q['options'] = new_opts
            q['answer'] = target_idx
            letter = option_letters[target_idx]
            letter_counts[letter] += 1
            total_shuffled += 1

print(f"Option position balancing complete: {total_shuffled} questions.")
print(f"Balanced answer distribution: {letter_counts}")

# Write updated cases_seed.json
with open('cases_seed.json', 'w', encoding='utf-8') as f:
    json.dump(cases, f, indent=2, ensure_ascii=False)

# Update SQLite Database
conn = sqlite3.connect('tracex.db')
c = conn.cursor()

c.execute("DELETE FROM questions")

for cid, case in cases.items():
    ev_list = case.get('evidence', [])
    r2_ev_list = case.get('round2Evidence', [])

    for r_num, r_key, evs in [(1, 'questions', ev_list), (2, 'round2Questions', r2_ev_list)]:
        for q_idx, q in enumerate(case.get(r_key, [])):
            qid = f"{cid}-r{r_num}-q{q_idx+1:02d}"
            opts = q['options']
            ans_letter = option_letters[q['answer']]
            ev_ref = evs[q_idx % len(evs)]['title'] if evs else ''
            now_iso = "2026-10-13T16:30:00Z"

            c.execute('''
                INSERT INTO questions (
                    id, case_id, round, order_num, question_text,
                    option_a, option_b, option_c, option_d,
                    correct_answer, marks, evidence_ref,
                    created_at, updated_at, updated_by
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                qid, cid, r_num, q_idx + 1, q['text'],
                opts[0], opts[1], opts[2], opts[3],
                ans_letter, 1, ev_ref,
                now_iso, now_iso, 'BALANCED_OPTIONS_UPDATE'
            ))

conn.commit()
conn.close()

# Update assets/js/investigation-data.js (STRIPPED of all answer keys)
inv_data_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'js', 'investigation-data.js')
client_cases = {}
for cid, case in cases.items():
    client_cases[cid] = {
        "id": case["id"],
        "name": case["name"],
        "summary": case["summary"],
        "evidence": case.get("evidence", []),
        "round2Evidence": case.get("round2Evidence", []),
        "questions": [
            {"text": q["text"], "options": q["options"]}
            for q in case.get("questions", [])
        ],
        "round2Questions": [
            {"text": q["text"], "options": q["options"]}
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

print(f"Updated {inv_data_path} successfully.")
