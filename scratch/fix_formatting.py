import os
import re

def fix_latex_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove space before \cite, \ref, \eqref
    content = re.sub(r' +(\\cite\{)', r'\1', content)
    content = re.sub(r' +(\\ref\{)', r'\1', content)
    content = re.sub(r' +(\\eqref\{)', r'\1', content)

    # 2. Remove space before period, Persian comma, colon, semicolon
    content = re.sub(r' +([.،:;])', r'\1', content)
    
    # 3. Fix spacing inside parentheses
    content = re.sub(r'\( +', '(', content)
    content = re.sub(r' +\)', ')', content)

    # 4. English comma to Persian comma (only if surrounded by Persian characters or at end of Persian word)
    # This is a bit risky but let's try a safe version:
    # Match a Persian word (using unicode range) followed by a comma
    content = re.sub(r'([\u0600-\u06FF]),', r'\1،', content)
    
    return content

files_to_fix = [
    '03_chapter1.tex',
    '04_chapter2.tex',
    '05_chapter3.tex',
    '06_chapter4.tex',
    '07_chapter5.tex'
]

for filename in files_to_fix:
    path = os.path.join(r'e:\projects\thesis_project', filename)
    if os.path.exists(path):
        fixed = fix_latex_file(path)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(fixed)
        print(f"Fixed {filename}")
