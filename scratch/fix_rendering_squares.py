import os
import re

# Persian digits mapping
persian_to_latin = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')

def fix_content(content):
    # 1. Wrap English terms in parentheses within section titles with \lr{}
    # Example: \subsection{آنتروپی اطلاعات (Shannon Entropy)} -> \subsection{آنتروپی اطلاعات (\lr{Shannon Entropy})}
    content = re.sub(r'(\\subsection\{[^{}]*)\(([a-zA-Z\s]+)\)([^{}]*\})', r'\1(\\lr{\2})\3', content)
    content = re.sub(r'(\\section\{[^{}]*)\(([a-zA-Z\s]+)\)([^{}]*\})', r'\1(\\lr{\2})\3', content)
    content = re.sub(r'(\\caption\{[^{}]*)\(([a-zA-Z\s]+)\)([^{}]*\})', r'\1(\\lr{\2})\3', content)

    # 2. Specifically fix the "NPCR و UACI" cases in titles
    content = content.replace('(NPCR و UACI)', '(\\lr{NPCR} و \\lr{UACI})')
    content = content.replace('(NPCR and UACI)', '(\\lr{NPCR} and \\lr{UACI})')
    
    # 3. Convert Persian digits to Latin in math mode
    def fix_math_digits(match):
        math_content = match.group(0)
        # Only translate digits, keep everything else
        return math_content.translate(persian_to_latin)

    # Patterns for math environments
    content = re.sub(r'\\begin\{equation\}.*?\\end\{equation\}', fix_math_digits, content, flags=re.DOTALL)
    content = re.sub(r'\\begin\{align\}.*?\\end\{align\}', fix_math_digits, content, flags=re.DOTALL)
    content = re.sub(r'\\begin\{cases\}.*?\\end\{cases\}', fix_math_digits, content, flags=re.DOTALL)
    content = re.sub(r'\$.*?\$', fix_math_digits, content) 
    
    # 4. Handle some specific edge cases seen in the image
    # If "H(m)" in a formula is broken, let's ensure it's not being treated as Persian text
    # Actually, math mode should handle it, but the Persian digits inside math might be the cause.
    
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
