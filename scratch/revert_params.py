import os
import re

def fix_content(content):
    # 1. Remove the problematic \lr{} from command arguments that caused "Missing number" errors
    content = content.replace('\\lr{0.31}', '0.31')
    content = content.replace('width=\\lr{0.6}', 'width=0.6')
    content = content.replace('width=\\lr{0.7}', 'width=0.7')
    content = content.replace('width=\\lr{0.8}', 'width=0.8')
    content = content.replace('width=\\lr{3}', 'width=3')
    
    # Generic removal of \lr{} from width/scale/vspace/hspace
    content = re.sub(r'(\\begin\{subfigure\}\{)\\lr\{([0-9\.]+)\}(\\textwidth\})', r'\1\2\3', content)
    content = re.sub(r'(width|scale|vspace|hspace)=\\lr\{([0-9\.]+)\}', r'\1=\2', content)
    content = re.sub(r'(\\vspace|\\hspace)\{\\lr\{([0-9\.]+)\}', r'\1{\2', content)

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
