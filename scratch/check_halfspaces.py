#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check for incorrect spacing in Persian text (space instead of ZWNJ)."""
import re, os, sys

sys.stdout.reconfigure(encoding='utf-8')

bad_patterns = [
    r'می [شکدتبپرزگف]',
    r'نمی [شکدتبپرزگف]',
    r'پیکسل ها',
    r'آن ها',
]

files = [
    '03_chapter1.tex', '04_chapter2.tex', '05_chapter3.tex',
    '06_chapter4.tex', '07_chapter5.tex', '08_references.tex'
]

for fname in files:
    if not os.path.exists(fname):
        continue
    with open(fname, encoding='utf-8') as f:
        content = f.read()
    lines = content.splitlines()
    issues = []
    for i, line in enumerate(lines, 1):
        for pat in bad_patterns:
            for m in re.finditer(pat, line):
                issues.append((i, m.group(), line.strip()[:80]))
    if issues:
        print(f"\n=== {fname}: {len(issues)} issues ===")
        for lineno, match, ctx in issues[:10]:
            # Print line number and just the match without full context to avoid encoding issues
            print(f"  Line {lineno}: pattern found")
    else:
        print(f"{fname}: OK")

print("\nDone.")
