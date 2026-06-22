"""Repair broken citations and glyph issues in thesis LaTeX sources."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(r"e:\projects\thesis_project_v2\thesis_latex_source")

PERSIAN_DIGITS = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")


def persian_digits_to_ascii(s: str) -> str:
    return s.translate(PERSIAN_DIGITS)


def fix_citations(text: str) -> tuple[str, int]:
    before = text.count(r"\textbackslash{}\lr{cite}\{")
    text = text.replace(r"\textbackslash{}\lr{cite}\{", r"\cite{")
    text = re.sub(
        r"\\lr\{ref\}([۰-۹0-9]+)",
        lambda m: "ref" + persian_digits_to_ascii(m.group(1)),
        text,
    )
    text = re.sub(r"\\lr\{ref(\d+)\}", r"ref\1", text)
    text = re.sub(r"\\cite\{([^}]*)\\\}", r"\\cite{\1}", text)
    return text, before


def fix_infinity_outside_verbatim(text: str) -> str:
    parts = text.split(r"\begin{verbatim}")
    out = []
    for i, chunk in enumerate(parts):
        if i > 0:
            chunk = r"\begin{verbatim}" + chunk
        body, tail = chunk.split(r"\end{verbatim}", 1) if r"\end{verbatim}" in chunk else (chunk, "")
        body = body.replace("∞", r"$\infty$")
        body = re.sub(
            r"\\lr\{PSNR\}\s*=\s*∞",
            r"\\lr{PSNR} = $\\infty$",
            body,
        )
        body = re.sub(
            r"\\lr\{PSNR\}\s*=\s*\\lr\{inf\}",
            r"\\lr{PSNR} = $\\infty$",
            body,
        )
        out.append(body + (r"\end{verbatim}" + tail if tail else ""))
    return "".join(out)


def process_file(path: Path) -> dict:
    original = path.read_text(encoding="utf-8")
    text = original
    text, cite_n = fix_citations(text)
    text = fix_infinity_outside_verbatim(text)
    if text != original:
        path.write_text(text, encoding="utf-8")
    return {"file": path.name, "cites": cite_n, "changed": text != original}


def patch_preamble() -> None:
    return


def patch_sync_inline() -> None:
    sync = Path(r"e:\projects\thesis_project_v2\sync_docx_to_latex.py")
    text = sync.read_text(encoding="utf-8")
    old = """def inline(text: str) -> str:
    text = convert_citations(text)
    text = wrap_lr(text)
    out: list[str] = []
    i = 0
    for m in re.finditer(r"\\\\(?:lr|cite)\\{[^{}]*\\}", text):
        out.append(esc_latex(text[i : m.start()]))
        out.append(m.group(0))
        i = m.end()
    out.append(esc_latex(text[i:]))
    return "".join(out)"""
    new = """def inline(text: str) -> str:
    protected: list[str] = []

    def protect(m: re.Match) -> str:
        protected.append(m.group(0))
        return f"@@PROT{len(protected) - 1}@@"

    text = convert_citations(text)
    text = re.sub(r"\\\\cite\\{[^{}]+\\}", protect, text)
    text = wrap_lr(text)
    text = esc_latex(text)
    for i, val in enumerate(protected):
        text = text.replace(f"@@PROT{i}@@", val)
    return text"""
    if old in text:
        sync.write_text(text.replace(old, new), encoding="utf-8")


def main() -> None:
    patch_preamble()
    patch_sync_inline()
    total_cites = 0
    changed_files = 0
    for path in sorted(ROOT.glob("*.tex")):
        if path.name == "preamble.tex":
            continue
        stats = process_file(path)
        total_cites += stats["cites"]
        if stats["changed"]:
            changed_files += 1
            print(f"fixed {path.name}: {stats['cites']} cites")
    print(f"Done. files_changed={changed_files}, cites_fixed={total_cites}")


if __name__ == "__main__":
    main()
