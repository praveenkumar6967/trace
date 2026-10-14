import json

with open('cases_seed.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

with open('cases_summary.txt', 'w', encoding='utf-8') as out:
    for cid, c in d.items():
        out.write(f"=== {cid}: {c.get('name')} ===\n")
        out.write(f"Summary: {c.get('summary')}\n")
        out.write("ROUND 1 EVIDENCE:\n")
        for e in c.get('evidence', []):
            out.write(f"  [{e.get('tag')}] {e.get('title')} ({e.get('time', '')}): {e.get('details')}\n")
        out.write("ROUND 2 EVIDENCE:\n")
        for e in c.get('round2Evidence', []):
            out.write(f"  [{e.get('tag')}] {e.get('title')} ({e.get('time', '')}): {e.get('details')}\n")
        out.write("\n")

print("Saved cases_summary.txt")
