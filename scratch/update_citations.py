import os
import re

files = [f for f in os.listdir('.') if f.endswith('.tex')]

for filename in files:
    if filename == '08_references.tex' or filename == '08_references_new.tex':
        continue
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace \cite{...} with \citep{...}
    new_content = re.sub(r'\\cite\{', r'\\citep{', content)
    
    if new_content != content:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated citations in {filename}")
