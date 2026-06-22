"""Fix bidi-related rendering issues in thesis LaTeX sources."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(r"e:\projects\thesis_project_v2\thesis_latex_source")
CHAPTER_GLOB = ("02_abstract.tex", "03_chapter1.tex", "04_chapter2.tex", "05_chapter3.tex", "06_chapter4.tex", "07_chapter5.tex")


def fix_powers(text: str) -> str:
    replacements = [
        ("10\\textasciicircum{}105", "$10^{105}$"),
        ("2\\textasciicircum{}348", "$2^{348}$"),
        ("2\\textasciicircum{}256", "$2^{256}$"),
        ("10\\textasciicircum{}15", "$10^{-15}$"),
        ("\\textasciitilde{}10105", "$\\sim 10^{105}$"),
        ("\\textasciitilde{}۶.۷۶", "$\\sim 6.76$"),
        ("10⁻¹⁵", "$10^{-15}$"),
        ("۱۰⁻¹⁵", "$10^{-15}$"),
        ("۱۰¹⁰⁵", "$10^{105}$"),
        ("10¹⁴", "$10^{14}$"),
        ("10¹⁰⁵", "$10^{105}$"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def fix_misc_glyphs(text: str) -> str:
    text = text.replace("]۶،۷،۱۲ [", r"\cite{ref6, ref7, ref12}")
    text = text.replace("¬", r"\lr{$\neg$}")
    text = re.sub(r"(?<![\\$])\bμ\b", r"$\\mu$", text)
    text = text.replace("—", r"{-}--")
    text = text.replace("–", r"{-}-")
    return text


def fix_keyspace_table(text: str) -> str:
    old = """\\begin{table}[h]
\\centering
\\small
\\begin{tabular}{ll}
\\hline
تخمین اندازه فضای کلید &  \\\\
\\hline
\\end{tabular}
\\end{table}"""
    new = """\\begin{equation}
|K| \\approx 10^{15 \\times 7} = 10^{105} > 2^{348}
\\label{eq:keyspace}
\\end{equation}"""
    return text.replace(old, new)


def process_file(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    text = original
    text = fix_powers(text)
    text = fix_misc_glyphs(text)
    if path.name == "05_chapter3.tex":
        text = fix_keyspace_table(text)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = 0
    for name in CHAPTER_GLOB:
        path = ROOT / name
        if path.exists() and process_file(path):
            print(f"fixed {name}")
            changed += 1
    print(f"Done. files_changed={changed}")


if __name__ == "__main__":
    main()
