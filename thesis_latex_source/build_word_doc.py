import os
import re
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_TEX_PATH = os.path.join(SCRIPT_DIR, "main.tex")
WORD_BUILD_DIR = os.path.join(SCRIPT_DIR, "word-build")
MERGED_TEX_PATH = os.path.join(WORD_BUILD_DIR, "_merged.tex")
OUTPUT_DOCX_PATH = os.path.join(WORD_BUILD_DIR, "thesis.docx")
ROOT_DOCX_PATH = os.path.join(os.path.dirname(SCRIPT_DIR), "main_updated.docx")
REF_DOCX_PATH = os.path.join(WORD_BUILD_DIR, "reference.docx")

def build_merged_tex():
    if not os.path.exists(MAIN_TEX_PATH):
        raise FileNotFoundError(f"main.tex not found at {MAIN_TEX_PATH}")

    os.makedirs(WORD_BUILD_DIR, exist_ok=True)

    with open(MAIN_TEX_PATH, "r", encoding="utf-8") as f:
        main_content = f.read()

    # Extract body within \begin{document} ... \end{document}
    doc_match = re.search(r"\\begin\{document\}(.*?)\\end\{document\}", main_content, re.DOTALL)
    body = doc_match.group(1) if doc_match else main_content

    def replace_input(match):
        rel_path = match.group(1).strip()
        if rel_path == "preamble":
            return ""
        if not rel_path.endswith(".tex"):
            rel_path += ".tex"
        
        full_path = os.path.join(SCRIPT_DIR, rel_path)
        if os.path.exists(full_path):
            with open(full_path, "r", encoding="utf-8") as tf:
                content = tf.read()
            return f"\n% --- BEGIN {rel_path} ---\n" + content + f"\n% --- END {rel_path} ---\n"
        else:
            print(f"Warning: input file not found: {full_path}")
            return f"% File not found: {rel_path}\n"

    # Replace \input{...} recursively or singly
    merged = re.sub(r"\\input\{([^}]+)\}", replace_input, body)

    with open(MERGED_TEX_PATH, "w", encoding="utf-8") as f:
        f.write(merged)
    
    print(f"Successfully generated merged LaTeX file: {MERGED_TEX_PATH}")

def run_pandoc():
    if not os.path.exists(MERGED_TEX_PATH):
        raise FileNotFoundError(f"_merged.tex not found at {MERGED_TEX_PATH}")
    
    cmd = [
        "pandoc",
        MERGED_TEX_PATH,
        "-o", OUTPUT_DOCX_PATH,
        f"--reference-doc={REF_DOCX_PATH}"
    ]
    
    print("Running Pandoc conversion...")
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=SCRIPT_DIR)
    
    if result.returncode == 0:
        print(f"Successfully compiled Word document: {OUTPUT_DOCX_PATH}")
        # Also copy to root main_updated.docx
        import shutil
        shutil.copyfile(OUTPUT_DOCX_PATH, ROOT_DOCX_PATH)
        print(f"Updated reference copy: {ROOT_DOCX_PATH}")
    else:
        print("Pandoc build failed with stderr:")
        print(result.stderr)

if __name__ == "__main__":
    build_merged_tex()
    run_pandoc()
