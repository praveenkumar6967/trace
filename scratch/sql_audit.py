import re

with open('server.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

suspicious = []
for idx, line in enumerate(lines, 1):
    if 'c.execute(' in line or 'c.executescript(' in line:
        if ('f"' in line or "f'" in line or ' % ' in line or '.format(' in line) and '?' not in line:
            suspicious.append((idx, line.strip()))

print(f'Total suspicious execute lines: {len(suspicious)}')
for ln, l in suspicious:
    print(f'Line {ln}: {l}')
