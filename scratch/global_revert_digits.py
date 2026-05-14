import os

persian_to_latin = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')

def fix_content(content):
    # 1. Revert all Persian digits to Latin digits
    content = content.translate(persian_to_latin)
    
    # 2. Ensure decimal separator is dot in source
    # (My previous script already did some of this, but let's be sure)
    content = content.replace('\u066b', '.')
    
    return content

files = [
    '01_titlepage.tex',
    '01_bismillah.tex',
    '01_jury.tex',
    '01_originality.tex',
    '01_ethics.tex',
    '02_dedication.tex',
    '02_acknowledgments.tex',
    '02_frontmatter.tex',
    '02_abbreviations.tex',
    '02_abstract.tex',
    '03_chapter1.tex',
    '04_chapter2.tex',
    '05_chapter3.tex',
    '06_chapter4.tex',
    '07_chapter5.tex',
    '08_references.tex',
    '09_appendix.tex',
    '10_abstract_en.tex',
    '11_titlepage_en.tex',
    'main.tex',
    'preamble.tex'
]

for file_path in files:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = fix_content(content)
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'Fixed {file_path}')
        else:
            print(f'No changes in {file_path}')
