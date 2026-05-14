import os

def fix_content(content):
    # Replace Persian decimal separator with Latin dot
    # because B Lotus seems to lack the U+066B glyph
    content = content.replace('\u066b', '.')
    return content

files = [
    '03_chapter1.tex',
    '04_chapter2.tex',
    '05_chapter3.tex',
    '06_chapter4.tex',
    '07_chapter5.tex'
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
