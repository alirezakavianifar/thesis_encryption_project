import os
import re
import subprocess
from projectcfg import CFG

def resolve_inputs(tex_filepath, visited=None):
    if visited is None:
        visited = set()
    
    if tex_filepath in visited:
        return ""
    visited.add(tex_filepath)

    if not os.path.exists(tex_filepath):
        print(f"Warning: input file not found: {tex_filepath}")
        return f"% Missing file: {tex_filepath}\n"

    with open(tex_filepath, "r", encoding="utf-8") as f:
        content = f.read()

    def replacer(match):
        sub_name = match.group(1).strip()
        if sub_name == "preamble" or sub_name == "preamble.tex":
            return ""
        if not sub_name.endswith(".tex"):
            sub_name += ".tex"
        sub_path = os.path.join(os.path.dirname(tex_filepath), sub_name)
        return resolve_inputs(sub_path, visited)

    content = re.sub(r"\\input\{([^}]+)\}", replacer, content)

    def verbatim_replacer(match):
        v_file = match.group(1).strip()
        v_path = os.path.join(os.path.dirname(tex_filepath), v_file)
        if not os.path.exists(v_path):
            alt_path = os.path.join(CFG.latex_source_dir, v_file)
            if os.path.exists(alt_path):
                v_path = alt_path
        if os.path.exists(v_path):
            with open(v_path, "r", encoding="utf-8") as vf:
                v_code = vf.read()
            return f"\n\\begin{{verbatim}}\n{v_code}\n\\end{{verbatim}}\n"
        else:
            print(f"Warning: Verbatim file not found: {v_path}")
            return f"% Missing verbatim file: {v_file}\n"

    content = re.sub(r"\\(?:VerbatimInput|lstinputlisting)(?:\[[^\]]*\])?\{([^}]+)\}", verbatim_replacer, content)
    return content

def preprocess_latex_for_pandoc(text):
    # Extract \begin{document} ... \end{document} if present
    doc_match = re.search(r"\\begin\{document\}(.*?)\\end\{document\}", text, re.DOTALL)
    if doc_match:
        text = doc_match.group(1)

    # 1. Clean math environments containing \lr{...} which Pandoc fails to parse
    # e.g., \begin{align} ... \lr{LEL} ... \end{align} -> convert \lr{XYZ} inside math to \mathrm{XYZ}
    def clean_math_block(m):
        math_content = m.group(0)
        # Replace \lr{text} with \mathrm{text} inside math
        cleaned = re.sub(r"\\lr\{([^}]+)\}", r"\\mathrm{\1}", math_content)
        return cleaned

    text = re.sub(r"\\begin\{(align|equation|gather)\*?\}(.*?)\\end\{\1\*?\}", clean_math_block, text, flags=re.DOTALL)

    # 2. Convert \newpage, \clearpage into @@PB@@ sentinels
    text = re.sub(r"\\(newpage|clearpage)", r"\n\n@@PB@@\n\n", text)
    text = re.sub(r"\\tableofcontents", r"\n\n@@TOC@@\n\n", text)
    text = re.sub(r"\\listoftables", r"\n\n@@LOT@@\n\n", text)
    text = re.sub(r"\\listoffigures", r"\n\n@@LOF@@\n\n", text)

    # 3. Convert \begin{center} and \end{center} into @@CENTER_START@@ / @@CENTER_END@@ sentinels
    text = re.sub(r"\\begin\{center\}", r"\n\n@@CENTER_START@@\n\n", text)
    text = re.sub(r"\\end\{center\}", r"\n\n@@CENTER_END@@\n\n", text)

    # Auto-number sections and subsections with Persian section numbers (۱-۱, ۱-۲, ۲-۱, ۴-۵, etc.)
    def to_fa(n):
        return str(n).translate(str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹'))

    lines = text.split('\n')
    new_lines = []
    c_num = 0
    s_num = 0
    ss_num = 0

    for line in lines:
        ch_m = re.search(r"\\chapter\{([^}]+)\}", line)
        if ch_m:
            ch_title = ch_m.group(1)
            if "اول" in ch_title or "کلیات" in ch_title: c_num = 1
            elif "دوم" in ch_title or "مفاهیم" in ch_title: c_num = 2
            elif "سوم" in ch_title or "معرفی" in ch_title: c_num = 3
            elif "چهارم" in ch_title or "پیاده" in ch_title: c_num = 4
            elif "پنجم" in ch_title or "بحث" in ch_title: c_num = 5
            else: c_num = 0
            s_num = 0
            ss_num = 0
            new_lines.append(line)
            continue

        sec_m = re.search(r"\\section\{((?:[^{}]|\{[^{}]*\})+)\}", line)
        if sec_m and c_num > 0:
            title = sec_m.group(1).strip()
            if not re.match(r"^[\u06f0-\u06f90-9]+[\-\s]", title):
                s_num += 1
                ss_num = 0
                sss_num = 0
                prefix = f"\u200f{to_fa(c_num)}\u200f-\u200f{to_fa(s_num)}\u200f"
                line = f"\\section{{{prefix} {title}}}"
            new_lines.append(line)
            continue

        subsec_m = re.search(r"\\subsection\{((?:[^{}]|\{[^{}]*\})+)\}", line)
        if subsec_m and c_num > 0 and s_num > 0:
            title = subsec_m.group(1).strip()
            if not re.match(r"^[\u06f0-\u06f90-9]+[\-\s]", title):
                ss_num += 1
                sss_num = 0
                prefix = f"\u200f{to_fa(c_num)}\u200f-\u200f{to_fa(s_num)}\u200f-\u200f{to_fa(ss_num)}\u200f"
                line = f"\\subsection{{{prefix} {title}}}"
            new_lines.append(line)
            continue

        subsubsec_m = re.search(r"\\subsubsection\{((?:[^{}]|\{[^{}]*\})+)\}", line)
        if subsubsec_m and c_num > 0 and s_num > 0:
            title = subsubsec_m.group(1).strip()
            if not re.match(r"^[\u06f0-\u06f90-9]+[\-\s]", title):
                sss_num += 1
                if ss_num > 0:
                    prefix = f"\u200f{to_fa(c_num)}\u200f-\u200f{to_fa(s_num)}\u200f-\u200f{to_fa(ss_num)}\u200f-\u200f{to_fa(sss_num)}\u200f"
                else:
                    prefix = f"\u200f{to_fa(c_num)}\u200f-\u200f{to_fa(s_num)}\u200f-\u200f{to_fa(sss_num)}\u200f"
                line = f"\\subsubsection{{{prefix} {title}}}"
            new_lines.append(line)
            continue

        new_lines.append(line)

    text = '\n'.join(new_lines)

    # 4. Standardize Chapter titles with Persian Chapter numbers (فصل اول..پنجم & مراجع)
    text = re.sub(r"\\chapter\{کلیات تحقیق\}", r"\\chapter{فصل اول: کلیات تحقیق}", text)
    text = re.sub(r"\\chapter\{مفاهیم پایه و پیشینه پژوهش\}", r"\\chapter{فصل دوم: مفاهیم پایه و پیشینه پژوهش}", text)
    text = re.sub(r"\\chapter\{معرفی الگوریتم پیشنهادی\}", r"\\chapter{فصل سوم: معرفی الگوریتم پیشنهادی}", text)
    text = re.sub(r"\\chapter\{پیاده[\s\u200c]*سازی و ارزیابی تجربی الگوریتم\}", r"\\chapter{فصل چهارم: پیاده‌سازی و ارزیابی تجربی الگوریتم}", text)
    text = re.sub(r"\\chapter\{بحث و نتیجه[\s\u200c]*گیری\}", r"\\chapter{فصل پنجم: بحث و نتیجه‌گیری}", text)

    # Convert thebibliography environment to clean Heading 1 for References
    text = re.sub(r"\\begin\{thebibliography\}\{[^}]*\}", r"\n\n\\chapter*{فهرست مراجع}\n\n", text)
    text = re.sub(r"\\end\{thebibliography\}", r"", text)

    # Standardize BiDi order for NIST SP 800-22 using RLM (\u200f)
    text = re.sub(r"NIST\s+SP[\s\u200c\-]*800[\s\u200c\-]*22", "NIST SP\u200f 800-22", text)

    # 5. Convert custom macros & XePersian commands to standard LaTeX
    text = text.replace('\u0640', '') # Strip Tatweel/Kashida \u0640
    text = re.sub(r"\\imdims\{([^}]+)\}\{([^}]+)\}", r"\1" + chr(0x00a0) + "×" + chr(0x00a0) + r"\2", text)
    text = re.sub(r"\\imdim\{([^}]+)\}", r"\1" + chr(0x00a0) + "×" + chr(0x00a0) + r"\1", text)

    # Standardize BiDi order for Latin acronyms followed by Persian parentheses (e.g., RGB (قرمز، سبز، آبی))
    text = re.sub(r"([A-Za-z0-9\-]{2,})\s*(\([\u0600-\u06FF\s،؛]{2,}\))", chr(0x200f) + r"\1 \2", text)

    text = re.sub(r"\\lr\{([^}]*)\}", r"\1", text)
    text = re.sub(r"\\rl\{([^}]*)\}", r"\1", text)
    text = re.sub(r"\\Latincite\{([^}]*)\}", r"\\cite{\1}", text)
    text = text.replace(r"\pyver", "Python 3.10")
    text = re.sub(r"\\SepMark\{[^}]*\}", "", text)

    # 5. Strip XePersian / bidi specific environments & commands Pandoc does not understand
    text = re.sub(r"\\begin\{(latin|persian|NoHyper|LTRbibitems)\}", "", text)
    text = re.sub(r"\\end\{(latin|persian|NoHyper|LTRbibitems)\}", "", text)
    text = re.sub(r"\\resetlatinfont", "", text)

    # 3. Convert \pagenumbering{harfi} / \pagenumbering{arabic}
    text = re.sub(r"\\pagenumbering\{[^}]+\}", "", text)

    # 4. Clean xepersian specific font commands
    text = re.sub(r"\\settextfont\[.*?\]\{.*?\}", "", text)
    text = re.sub(r"\\setdigitfont\[.*?\]\{.*?\}", "", text)
    text = re.sub(r"\\setlatintextfont\[.*?\]\{.*?\}", "", text)

    # 4. Standardize graphicx image paths (only inside \includegraphics)
    def fix_img_path(m):
        opts = m.group(1) or ""
        path = m.group(2).replace("\\", "/")
        return f"\\includegraphics{opts}{{{path}}}"

    text = re.sub(r"\\includegraphics(\[[^\]]*\])?\{([^}]+)\}", fix_img_path, text)

    # 6. Auto-number figure and table captions & resolve LaTeX labels and references (\eqref, \ref)
    label_map = {}
    ch_num = 0
    eq_num = 0
    fig_num = 0
    tab_num = 0
    in_env = None
    new_lines = []

    lines = text.split('\n')
    for line in lines:
        ch_m = re.search(r"\\chapter\*?\{([^}]+)\}", line)
        if ch_m:
            t = ch_m.group(1)
            if 'اول' in t or 'کلیات' in t: ch_num = 1
            elif 'دوم' in t or 'مفاهیم' in t: ch_num = 2
            elif 'سوم' in t or 'معرفی' in t: ch_num = 3
            elif 'چهارم' in t or 'پیاده' in t: ch_num = 4
            elif 'پنجم' in t or 'بحث' in t: ch_num = 5
            else: ch_num = 0
            eq_num = 0
            fig_num = 0
            tab_num = 0

        if re.search(r"\\begin\{(figure|table)\}", line):
            env_m = re.search(r"\\begin\{(figure|table)\}", line)
            in_env = env_m.group(1)
            if in_env == 'figure': fig_num += 1
            if in_env == 'table': tab_num += 1

        if re.search(r"\\begin\{(equation|align|gather)\*?\}", line):
            eq_num += 1

        cap_m = re.search(r"\\caption(?:\[[^\]]*\])?\{((?:[^{}]|\{[^{}]*\})+)\}", line)
        if cap_m and in_env:
            cap_txt = cap_m.group(1).strip()
            cap_txt = re.sub(r"\s*\.\s*$", "", cap_txt)
            if in_env == 'figure':
                if not cap_txt.startswith("شکل"):
                    prefix = f"شکل \u200f{to_fa(ch_num)}\u200f-\u200f{to_fa(fig_num)}\u200f: "
                    line = line.replace(cap_m.group(0), f"\\caption{{{prefix}{cap_txt}}}")
            elif in_env == 'table':
                if not cap_txt.startswith("جدول"):
                    prefix = f"جدول \u200f{to_fa(ch_num)}\u200f-\u200f{to_fa(tab_num)}\u200f: "
                    line = line.replace(cap_m.group(0), f"\\caption{{{prefix}{cap_txt}}}")

        for lbl in re.findall(r"\\label\{([^}]+)\}", line):
            if lbl.startswith('eq:'):
                label_map[lbl] = f"(\u200f{to_fa(ch_num)}\u200f-\u200f{to_fa(eq_num)}\u200f)"
            elif lbl.startswith('tab:'):
                label_map[lbl] = f"\u200f{to_fa(ch_num)}\u200f-\u200f{to_fa(tab_num)}\u200f"
            elif lbl.startswith('fig:'):
                label_map[lbl] = f"\u200f{to_fa(ch_num)}\u200f-\u200f{to_fa(fig_num)}\u200f"
            else:
                label_map[lbl] = f"(\u200f{to_fa(ch_num)}\u200f-\u200f{to_fa(eq_num)}\u200f)"

        if re.search(r"\\end\{(figure|table)\}", line):
            in_env = None

        new_lines.append(line)

    text = '\n'.join(new_lines)

    def eqref_sub(m):
        lbl = m.group(1).strip()
        return label_map.get(lbl, f"({lbl})")

    def ref_sub(m):
        lbl = m.group(1).strip()
        return label_map.get(lbl, lbl)

    text = re.sub(r"\\eqref\{([^}]+)\}", eqref_sub, text)
    text = re.sub(r"\\ref\{([^}]+)\}", ref_sub, text)
    text = re.sub(r"\\label\{[^}]+\}", "", text)

    return text

def assemble_and_build():
    print(f"Reading main LaTeX file: {CFG.main_tex}")
    full_latex = resolve_inputs(CFG.main_tex)
    cleaned_latex = preprocess_latex_for_pandoc(full_latex)

    with open(CFG.merged_tex, "w", encoding="utf-8") as f:
        f.write(cleaned_latex)
    
    print(f"assembled merged LaTeX: {CFG.merged_tex}")

    # Build resource paths for pandoc
    resource_paths = [
        CFG.latex_source_dir,
        os.path.join(CFG.latex_source_dir, "images"),
        os.path.join(CFG.latex_source_dir, "outputs")
    ]
    resource_arg = ";".join(resource_paths) if os.name == 'nt' else ":".join(resource_paths)

    cmd = [
        "pandoc",
        "-f", "latex",
        CFG.merged_tex,
        "-t", "docx",
        "--reference-doc", CFG.reference_docx,
        "--resource-path", resource_arg,
        "-o", CFG.intermediate_docx
    ]

    print("running pandoc:", " ".join(cmd))
    res = subprocess.run(cmd, capture_output=True, text=True, cwd=CFG.latex_source_dir)
    
    if res.returncode == 0:
        print(f"pandoc done -> {CFG.intermediate_docx}")
    else:
        print("pandoc failed:")
        print(res.stderr)
        raise RuntimeError("Pandoc conversion failed.")

if __name__ == "__main__":
    assemble_and_build()
