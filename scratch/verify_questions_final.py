# scratch/verify_questions_final.py
import sqlite3
import json
import os

conn = sqlite3.connect('tracex.db')
c = conn.cursor()

print("--- SQLITE QUESTIONS TABLE AUDIT ---")
c.execute("SELECT COUNT(*) FROM questions")
total_q = c.fetchone()[0]
print(f"Total Questions in DB: {total_q} (Expected: 450)")
assert total_q == 450

c.execute("SELECT case_id, round, COUNT(*) FROM questions GROUP BY case_id, round ORDER BY case_id, round")
buckets = c.fetchall()
print(f"Total Case-Round buckets: {len(buckets)} (Expected: 30)")
assert len(buckets) == 30
assert all(b[2] == 15 for b in buckets)

c.execute("SELECT COUNT(*) FROM questions WHERE option_a = '' OR option_b = '' OR option_c = '' OR option_d = ''")
empty_opts = c.fetchone()[0]
print(f"Empty option count: {empty_opts} (Expected: 0)")
assert empty_opts == 0

c.execute("SELECT COUNT(*) FROM questions WHERE correct_answer NOT IN ('A', 'B', 'C', 'D')")
invalid_keys = c.fetchone()[0]
print(f"Invalid answer keys: {invalid_keys} (Expected: 0)")
assert invalid_keys == 0

c.execute("SELECT correct_answer, COUNT(*) FROM questions GROUP BY correct_answer ORDER BY correct_answer")
dist = c.fetchall()
print(f"Answer key distribution: {dist}")

# Check for duplicate question texts in DB
c.execute("SELECT case_id, round, question_text, COUNT(*) FROM questions GROUP BY case_id, round, LOWER(question_text) HAVING COUNT(*) > 1")
dup_q = c.fetchall()
print(f"Duplicate questions in DB: {len(dup_q)} (Expected: 0)")
assert len(dup_q) == 0

# Check cases_seed.json
print("\n--- CASES_SEED.JSON AUDIT ---")
with open('cases_seed.json', 'r', encoding='utf-8') as f:
    seed_data = json.load(f)

print(f"Total cases in cases_seed.json: {len(seed_data)} (Expected: 15)")
assert len(seed_data) == 15

seed_total = sum(len(c['questions']) + len(c['round2Questions']) for c in seed_data.values())
print(f"Total questions in cases_seed.json: {seed_total} (Expected: 450)")
assert seed_total == 450

# Check investigation-data.js
print("\n--- ASSETS/JS/INVESTIGATION-DATA.JS PRIVACY AUDIT ---")
with open('assets/js/investigation-data.js', 'r', encoding='utf-8') as f:
    inv_js = f.read()

assert '"answer":' not in inv_js, "SECURITY ALERT: answer found in investigation-data.js!"
assert '"correct_answer":' not in inv_js, "SECURITY ALERT: correct_answer found in investigation-data.js!"
print("Privacy verification passed: 0 answer keys exposed in client JS file.")

conn.close()
print("\n[ALL AUDITS PASSED WITH ZERO ERRORS]")
