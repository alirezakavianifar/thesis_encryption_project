import os
import re

def fix_content(content):
    content = content.replace('٪', '%')
    content = content.replace('٫', '.')
    # Replace / between Persian digits with .
    content = re.sub(r'([۰-۹])/([۰-۹])', r'\1.\2', content)
    return content

files = [
    '01_titlepage.tex', '01_bismillah.tex', '01_jury.tex', '01_originality.tex',
    '01_ethics.tex', '02_dedication.tex', '02_acknowledgments.tex',
    '02_frontmatter.tex', '02_abbreviations.tex', '02_abstract.tex',
    '10_abstract_en.tex', '03_chapter1.tex', '04_chapter2.tex',
    '05_chapter3.tex', '06_chapter4.tex', '07_chapter5.tex', '08_references.tex'
]

for filename in files:
    path = os.path.join('e:\\projects\\thesis_project', filename)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        new_content = fix_content(content)
        if new_content != content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Fixed {filename}")
