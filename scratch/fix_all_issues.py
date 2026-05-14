#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive fix script for thesis issues:
 1. Revert false-positive ZWNJs inserted after words ending in 'می' (suffix case)
 2. Replace '/' decimal separator with '٫' (U+066B) in Chapter 4 table numbers
 3. Replace Latin '.' decimal separator with '٫' in NPCR/UACI table
"""
import re, sys
sys.stdout.reconfigure(encoding='utf-8')

ZWNJ = '\u200c'
ARABIC_DECIMAL = '\u066b'  # ٫  Persian decimal separator

def fix_false_positive_zwnjs(content):
    """
    Revert ZWNJs that were erroneously inserted between a word ending in 'می'
    (suffix) and the following word.  The heuristic: if the character immediately
    BEFORE 'می' is a Persian letter (not a space), then 'می' is a suffix of that
    word, not a verb-prefix, so the ZWNJ is wrong.

    Persian letters: U+0600–U+06FF range (covers Arabic/Persian script).
    We use a conservative set of the most-common word-ending letters that
    appear before 'می' as suffix: ل, ن, ت, م, د, ز, ک, ق, س, ف, ع, و, ا, ر, ی, ه, ب, پ.
    """
    # Revert [Persian letter]می‌[word] → [Persian letter]می [word]
    # Only when the character before می is a Persian word-body letter.
    # We match one Persian letter before می‌ and undo the ZWNJ.
    fixed = re.sub(
        r'([ا-ی])می' + ZWNJ + r'([ا-ی])',
        r'\1می \2',
        content
    )
    return fixed

def re_apply_correct_zwnjs(content):
    """
    Re-apply ZWNJ correctly: only when 'می' appears as a STANDALONE word,
    i.e. preceded by a space (or newline / start-of-string), followed by a
    verb-stem starting letter.

    Verb stems commonly start with: ش، ک، د، ت، ب، پ، ر، ز، گ، ف، خ، ی، ه
    We exclude و (conjunction 'and') and آ (imperative ب+آ) to avoid false positives.
    """
    # Verb-start letters (excluding و which is also conjunction)
    verb_starts = 'شکدتبپرزگفخیه'
    # Match می preceded by space/newline/start, followed by space then verb-start
    fixed = re.sub(
        r'(?<= )می ([' + verb_starts + r'])',
        'می' + ZWNJ + r'\1',
        content
    )
    # Also handle line-start cases
    fixed = re.sub(
        r'^می ([' + verb_starts + r'])',
        'می' + ZWNJ + r'\1',
        fixed,
        flags=re.MULTILINE
    )
    return fixed

def fix_decimal_separators_ch4(content):
    """
    Replace '/' used as decimal separator between Persian digits with '٫'.
    Persian digits: ۰-۹ (U+06F0–U+06F9).
    Only replace '/' that is flanked by Persian digit characters.
    """
    persian_digit = '[۰-۹]'
    # Pattern: persian_digit / persian_digit  → persian_digit ٫ persian_digit
    fixed = re.sub(
        r'(' + persian_digit + r')/' + r'(' + persian_digit + r')',
        r'\1' + ARABIC_DECIMAL + r'\2',
        content
    )
    return fixed

def fix_latin_dot_in_npcr_table(content):
    """
    Replace Latin '.' decimal separator with '٫' between Persian digits
    (handles cases like ۹۹.۶۱ → ۹۹٫۶۱).
    """
    persian_digit = '[۰-۹]'
    fixed = re.sub(
        r'(' + persian_digit + r')\.' + r'(' + persian_digit + r')',
        r'\1' + ARABIC_DECIMAL + r'\2',
        content
    )
    return fixed

# ── Chapter files that need ZWNJ false-positive correction ──────────────────
zwnj_files = [
    '03_chapter1.tex',
    '04_chapter2.tex',
    '05_chapter3.tex',
    '06_chapter4.tex',
    '07_chapter5.tex',
]

print("=== Step 1: Fix false-positive ZWNJs ===")
for fname in zwnj_files:
    with open(fname, encoding='utf-8') as f:
        original = f.read()

    fixed = fix_false_positive_zwnjs(original)
    fixed = re_apply_correct_zwnjs(fixed)

    if fixed != original:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(fixed)
        changed = sum(1 for a, b in zip(original.splitlines(), fixed.splitlines()) if a != b)
        print(f"  FIXED {fname}: {changed} line(s) changed")
    else:
        print(f"  OK    {fname}: no changes")

# ── Chapter 4: fix decimal separator ────────────────────────────────────────
print("\n=== Step 2: Fix decimal separators in Chapter 4 ===")
with open('06_chapter4.tex', encoding='utf-8') as f:
    ch4 = f.read()

ch4_fixed = fix_decimal_separators_ch4(ch4)
ch4_fixed = fix_latin_dot_in_npcr_table(ch4_fixed)

if ch4_fixed != ch4:
    with open('06_chapter4.tex', 'w', encoding='utf-8') as f:
        f.write(ch4_fixed)
    changed = sum(1 for a, b in zip(ch4.splitlines(), ch4_fixed.splitlines()) if a != b)
    print(f"  FIXED 06_chapter4.tex: {changed} line(s) changed")
else:
    print("  OK    06_chapter4.tex: no decimal separator changes needed")

# ── Chapter 2: fix Latin dots in body text (e.g. ۷.۹۴۶۱) ─────────────────
print("\n=== Step 3: Fix Latin decimal dots in Chapter 2 body text ===")
with open('04_chapter2.tex', encoding='utf-8') as f:
    ch2 = f.read()

ch2_fixed = fix_latin_dot_in_npcr_table(ch2)   # same regex works
if ch2_fixed != ch2:
    with open('04_chapter2.tex', 'w', encoding='utf-8') as f:
        f.write(ch2_fixed)
    changed = sum(1 for a, b in zip(ch2.splitlines(), ch2_fixed.splitlines()) if a != b)
    print(f"  FIXED 04_chapter2.tex: {changed} line(s) changed")
else:
    print("  OK    04_chapter2.tex: no changes")

print("\nAll done.")
