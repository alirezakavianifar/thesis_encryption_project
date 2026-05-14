import os

def fix_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Revert Persian decimal separator to slash for compatibility with B Lotus
    content = content.replace('٫', '/')
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

files = ['02_abstract.tex', '03_chapter1.tex', '04_chapter2.tex', '05_chapter3.tex', '06_chapter4.tex', '07_chapter5.tex']
for f in files:
    if os.path.exists(f):
        fix_file(f)
