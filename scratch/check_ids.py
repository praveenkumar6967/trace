import re

def extract_ids(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    ids1 = re.findall(r"getElementById\(['\"]([^'\"]+)['\"]\)", content)
    ids2 = re.findall(r"querySelector\(['\"]#([a-zA-Z0-9_\-]+)['\"]\)", content)
    return set(ids1 + ids2)

app_ids = extract_ids('assets/js/app.js')
admin_ids = extract_ids('assets/js/admin.js')

print(f"app.js element IDs ({len(app_ids)}):")
for i in sorted(app_ids):
    print("  -", i)

print(f"\nadmin.js element IDs ({len(admin_ids)}):")
for i in sorted(admin_ids):
    print("  -", i)
