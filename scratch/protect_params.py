import os
import re

def fix_content(content):
    # 1. Wrap numeric widths and scales in \lr{} to protect them from XePersian mapping
    # This specifically targets subfigure width, graphics width/scale, etc.
    content = re.sub(r'(\\begin\{subfigure\})(\{)(0\.[0-9]+)(\\textwidth\})', r'\1{\\lr{\3}\4}', content)
    content = re.sub(r'(\\includegraphics\[[^\]]*)width=([0-9\.]+)(\\textwidth|\\linewidth|cm|in|pt)', r'\1width=\\lr{\2}\3', content)
    content = re.sub(r'(\\includegraphics\[[^\]]*)scale=([0-9\.]+)', r'\1scale=\\lr{\2}', content)
    content = re.sub(r'(\\vspace\{)([0-9\.]+)(em|ex|cm|mm|in|pt|\\baselineskip)', r'\1\\lr{\2}\3', content)
    content = re.sub(r'(\\hspace\{)([0-9\.]+)(em|ex|cm|mm|in|pt)', r'\1\\lr{\2}\3', content)

    # 2. Fix the specific subfigure width issue seen in Chapter 4
    # Replaces {0.31\textwidth} with {\lr{0.31}\textwidth}
    content = content.replace('{0.31\\textwidth}', '{\\lr{0.31}\\textwidth}')
    
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

# Fix main.tex redundant newpages
if os.path.exists('main.tex'):
    with open('main.tex', 'r', encoding='utf-8') as f:
        main_content = f.read()
    
    # Remove \newpage after abstract inputs if they already have it
    main_content = main_content.replace('\\input{02_abstract}\n\\newpage', '\\input{02_abstract}')
    main_content = main_content.replace('\\input{10_abstract_en}\n\\newpage', '\\input{10_abstract_en}')
    
    with open('main.tex', 'w', encoding='utf-8') as f:
        f.write(main_content)
    print('Fixed main.tex')
