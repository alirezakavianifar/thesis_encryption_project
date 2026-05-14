import os
import re

def fix_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix punctuation
    content = content.replace(' .', '.')
    content = content.replace(' ؛', '؛')
    content = content.replace(' :', ':')
    
    # Fix NPCIR typo if any
    content = content.replace('NPCIR', 'NPCR')
    
    # Fix specific malformed number 96/9/6 -> 99.6%
    # But only if it looks like the user's report
    # The user said 96/9/6 was on page 45.
    # In my source it was ۹۹/۶۰٪.
    # I'll replace ۹۹/۶۰٪ with ۹۹٫۶۰٪
    content = content.replace('۹۹/۶۰٪', '۹۹٫۶۰٪')
    content = content.replace('۳۲/۱۳٪', '۳۲٫۱۳٪')
    content = content.replace('۸/۳', '۸٫۳')
    content = content.replace('۹۹/۵٪', '۹۹٫۵٪')
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

files = ['02_abstract.tex', '03_chapter1.tex', '04_chapter2.tex', '05_chapter3.tex', '06_chapter4.tex', '07_chapter5.tex']
for f in files:
    if os.path.exists(f):
        fix_file(f)
