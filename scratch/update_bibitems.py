import re

def process_references(content):
    # Remove honorifics
    honorifics = ['دکتر ', 'مهندس ', 'استاد ', 'حجت الاسلام ', 'آیت الله ']
    for h in honorifics:
        content = content.replace(h, '')

    # Regex for Persian: \bibitem{key} Last, First. Year
    persian_pattern = r'\\bibitem\{(\w+)\}\s+([^.]+)\.\s+([۰-۹]{4})'
    
    def persian_rep(match):
        key, author, year = match.groups()
        last_name = author.split('،')[0].strip() if '،' in author else author.split(',')[0].strip()
        return f'\\bibitem[{last_name}({year})]{{{key}}} {author}. {year}'

    # Regex for Latin: \bibitem{key} Author List (Year).
    # Latin authors often have dots: Yin, H., Xu, Y., ...
    latin_pattern = r'\\bibitem\{(\w+)\}\s+([^(\n]+)\s+\((\d{4})\)\.'
    
    def latin_rep(match):
        key, authors, year = match.groups()
        # Extract the first author's last name
        first_author = authors.split('&')[0].split(',')[0].strip()
        return f'\\bibitem[{first_author}({year})]{{{key}}} {authors.strip()} ({year}).'

    content = re.sub(persian_pattern, persian_rep, content)
    content = re.sub(latin_pattern, latin_rep, content)
    return content

# Read the file
with open('08_references.tex', 'r', encoding='utf-8') as f:
    content = f.read()

new_content = process_references(content)

with open('08_references_new.tex', 'w', encoding='utf-8') as f:
    f.write(new_content)
