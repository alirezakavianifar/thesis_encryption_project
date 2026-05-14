#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix incorrect half-spaces (space instead of ZWNJ) in Persian LaTeX thesis files.
Also fix آن ها -> آن‌ها and پیکسل ها -> پیکسل‌ها patterns.
"""
import re, os, sys

sys.stdout.reconfigure(encoding='utf-8')

ZWNJ = '\u200c'  # Zero-width non-joiner (correct half-space in Persian)

def fix_halfspaces(content):
    """Replace incorrect spaces with ZWNJ in common Persian verb forms."""
    # می + space + verb-start consonant -> می‌ + verb
    # Common verb beginnings: ش(shod), ک(konad), د(dahad), ت(tavaned), ب(bashad/binad), پ(pardazad)
    # ر(rasad), ز(zanad), گ(girad), ف(fahmad), خ(khahand), ی(yabad)
    verb_chars = 'شکدتبپرزگفخیوه'
    
    # Fix می + space + verb
    content = re.sub(f'می ([{verb_chars}])', f'می{ZWNJ}\\1', content)
    # Fix نمی + space + verb
    content = re.sub(f'نمی ([{verb_chars}])', f'نمی{ZWNJ}\\1', content)
    # Fix پیکسل ها -> پیکسل‌ها
    content = content.replace('پیکسل ها', f'پیکسل{ZWNJ}ها')
    # Fix آن ها -> آن‌ها
    content = content.replace('آن ها', f'آن{ZWNJ}ها')
    
    return content

files = [
    '03_chapter1.tex',
    '04_chapter2.tex', 
    '05_chapter3.tex',
    '06_chapter4.tex',
    '07_chapter5.tex',
]

for fname in files:
    if not os.path.exists(fname):
        print(f"SKIP: {fname} not found")
        continue
    with open(fname, encoding='utf-8') as f:
        original = f.read()
    
    fixed = fix_halfspaces(original)
    
    if fixed != original:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(fixed)
        # Count changes
        orig_lines = original.splitlines()
        fixed_lines = fixed.splitlines()
        changes = sum(1 for a, b in zip(orig_lines, fixed_lines) if a != b)
        print(f"FIXED: {fname} ({changes} lines changed)")
    else:
        print(f"  OK: {fname} (no changes needed)")

print("\nHalf-space fix complete.")
